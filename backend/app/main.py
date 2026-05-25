"""
PRYSM FastAPI Backend — main.py
Simple, stable, demo-ready. In-memory storage only.
"""

import asyncio
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Literal

from dotenv import load_dotenv

# Load environment variables from the root .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.store import (
    save_document, list_documents, get_document, delete_document,
    save_risks, get_risks, list_all_risks,
    save_report, list_reports, get_report,
)
from app.parser import extract_text_from_file, parse_document
from app.risk_engine import generate_risks
from app.report_engine import generate_report, generate_session_report
from app.screening import screen_document
from app.llm_client import LLMServiceError, create_chat_completion

# ── Create uploads directory ─────────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "storage/uploads"))
if not UPLOAD_DIR.is_absolute():
    UPLOAD_DIR = PROJECT_DIR / UPLOAD_DIR
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR = Path(os.getenv("REPORT_DIR", "storage/reports"))
if not REPORT_DIR.is_absolute():
    REPORT_DIR = PROJECT_DIR / REPORT_DIR

DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"
DEFAULT_LLM_FALLBACK_MODEL = "gemma-4-26b"


def get_llm_model_config() -> dict:
    return {
        "primary_model": os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL),
        "fallback_model": os.getenv("LLM_FALLBACK_MODEL", DEFAULT_LLM_FALLBACK_MODEL),
        "has_groq_api_key": bool(os.getenv("GROQ_API_KEY")),
    }


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp with a frontend-friendly Z suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_filename(filename: str | None) -> str:
    """Keep only the uploaded file's basename."""
    return Path(filename or "unknown_file").name


def default_parsed_data() -> dict:
    return {
        "document_type": "unknown",
        "amount": "UNKNOWN",
        "date": "UNKNOWN",
        "gstin": "UNKNOWN",
        "invoice_number": "UNKNOWN",
        "vendor_name": "UNKNOWN",
    }


def failed_upload_document(file: UploadFile, error: str = "Failed to process this file") -> dict:
    document_id = f"doc_{uuid.uuid4().hex[:12]}"
    return {
        "id": document_id,
        "document_id": document_id,
        "filename": safe_filename(getattr(file, "filename", None)),
        "status": "failed",
        "content_type": getattr(file, "content_type", None) or "application/octet-stream",
        "size_bytes": 0,
        "uploaded_at": utc_now(),
        "error": error,
    }


def build_document_record(
    document_id: str,
    filename: str,
    content: bytes,
    content_type: str,
    uploaded_at: str,
) -> dict:
    """Extract, screen, and analyze a document without admitting irrelevant files."""
    try:
        raw_text = extract_text_from_file(content, filename)
    except Exception:
        raw_text = ""

    try:
        parsed_data = parse_document(raw_text)
    except Exception:
        parsed_data = default_parsed_data()

    screening = screen_document(filename, raw_text, parsed_data)
    doc = {
        "id": document_id,
        "document_id": document_id,
        "filename": filename,
        "status": "uploaded" if screening["audit_eligible"] else screening["decision"],
        "content_type": content_type,
        "size_bytes": len(content),
        "uploaded_at": uploaded_at,
        "data": parsed_data,
        "raw_text_preview": raw_text[:300] if raw_text else "",
        "screening": screening,
        "screening_reason": screening["reason"],
    }

    risks = []
    if screening["audit_eligible"]:
        try:
            risks = generate_risks(doc)
        except Exception:
            pass
    doc["risks"] = risks
    return doc


def is_audit_eligible(document: dict) -> bool:
    """Return whether a stored document is allowed into audit calculations."""
    return document.get("screening", {}).get("audit_eligible", True)


def public_report(report: dict) -> dict:
    """Keep server file paths out of API responses."""
    return {key: value for key, value in report.items() if not key.startswith("_")}


def public_document(document: dict) -> dict:
    """Keep storage details private while returning parsed document evidence."""
    return {key: value for key, value in document.items() if not key.startswith("_")}


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ConversationTurn] = Field(default_factory=list)


def _format_document_list(documents: list[dict]) -> str:
    if not documents:
        return "No files have been uploaded yet."

    lines = ["Uploaded files:"]
    for index, document in enumerate(documents, start=1):
        filename = document.get("filename", "unknown")
        document_id = document.get("document_id") or document.get("id", "unknown")
        status = document.get("status", "unknown")
        size_bytes = document.get("size_bytes", 0)
        doc_type = document.get("data", {}).get("document_type", "unknown")
        lines.append(
            f"{index}. {filename} ({document_id}) - {status}, {doc_type}, {size_bytes} bytes"
        )
    return "\n".join(lines)


def _risk_lines(risks: list[dict], limit: int = 6) -> list[str]:
    lines = []
    for index, risk in enumerate(risks[:limit], start=1):
        title = risk.get("title") or risk.get("type", "Untitled risk")
        severity = risk.get("severity", "Info")
        source = risk.get("source_document", "unknown document")
        recommendation = risk.get("recommendation", "Review source evidence and assign an owner.")
        lines.append(f"{index}. {severity}: {title} in {source}. Action: {recommendation}")
    return lines


def _format_risk_list(risks: list[dict]) -> str:
    if not risks:
        return "No active risks are currently stored for the uploaded documents."

    return "\n".join([f"There are {len(risks)} active risk flag(s):", *_risk_lines(risks, 10)])


def _select_document_for_review(documents: list[dict]) -> dict | None:
    if not documents:
        return None

    documents_with_risks = [document for document in documents if document.get("risks")]
    return documents_with_risks[0] if documents_with_risks else documents[0]


def _format_single_document_review(document: dict) -> str:
    filename = document.get("filename", "unknown")
    document_id = document.get("document_id") or document.get("id", "unknown")
    data = document.get("data", {})
    risks = document.get("risks", [])
    doc_type = data.get("document_type", "unknown")
    amount = data.get("amount", "UNKNOWN")
    date = data.get("date", "UNKNOWN")
    gstin = data.get("gstin", "UNKNOWN")

    lines = [
        f"I picked {filename} ({document_id}).",
        "",
        "Quick review:",
        f"- Type: {doc_type}",
        f"- Amount: {amount}",
        f"- Date: {date}",
        f"- GSTIN: {gstin}",
        f"- Risk flags: {len(risks)}",
    ]

    if risks:
        lines.extend(["", "Most important findings:", *_risk_lines(risks, 3)])
    else:
        lines.extend(["", "No active risks are currently attached to this document."])

    return "\n".join(lines)


def _format_readiness_review(documents: list[dict], risks: list[dict], reports: list[dict]) -> str:
    critical = sum(1 for risk in risks if risk.get("severity") == "Critical")
    warnings = sum(1 for risk in risks if risk.get("severity") == "Warning")
    info = sum(1 for risk in risks if risk.get("severity") == "Info")
    readiness_score = max(0, 100 - (critical * 20) - (warnings * 5))

    lines = [
        "Audit readiness review:",
        f"- Documents reviewed: {len(documents)}",
        f"- Active risks: {len(risks)} ({critical} critical, {warnings} warning, {info} info)",
        f"- Generated reports: {len(reports)}",
        f"- Estimated readiness score: {readiness_score}/100",
        "",
    ]

    if risks:
        lines.append("Most important gaps:")
        lines.extend(_risk_lines(risks, 5))
        lines.extend([
            "",
            "Recommended next actions:",
            "1. Resolve warning and critical items with missing source evidence first.",
            "2. Generate a report after remediation notes are added.",
            "3. Re-upload corrected evidence for documents with missing dates, amounts, or GSTINs.",
        ])
    else:
        lines.extend([
            "No active risk flags are currently stored.",
            "",
            "Recommended next actions:",
            "1. Generate an audit report for management review.",
            "2. Spot-check extracted fields against source documents.",
            "3. Upload any missing approvals or supporting schedules.",
        ])

    return "\n".join(lines)


def _format_evidence_checklist(documents: list[dict], risks: list[dict]) -> str:
    lines = [
        "Evidence to collect before sign-off:",
        "1. Source documents for every uploaded file, with filename and document ID referenced in the workpaper.",
        "2. Approval evidence for high-value or material items.",
        "3. Vendor/tax master evidence for GSTIN or identity gaps.",
        "4. Date or reporting-period support for documents with missing dates.",
        "5. Amount tie-outs to invoice totals, ledgers, bank statements, or supporting schedules.",
    ]

    if risks:
        lines.extend(["", "Risk-linked evidence priorities:"])
        for index, risk in enumerate(risks[:5], start=1):
            source = risk.get("source_document", "unknown document")
            recommendation = risk.get("recommendation", "Collect supporting evidence and reviewer notes.")
            lines.append(f"{index}. {source}: {recommendation}")

    lines.extend([
        "",
        f"Current scope: {len(documents)} uploaded document(s), {len(risks)} active risk flag(s).",
    ])
    return "\n".join(lines)


def _format_next_actions(documents: list[dict], risks: list[dict], reports: list[dict]) -> str:
    critical = [risk for risk in risks if risk.get("severity") == "Critical"]
    warnings = [risk for risk in risks if risk.get("severity") == "Warning"]

    lines = [
        "Recommended compliance actions for this week:",
        "1. Triage open risk flags by severity and affected document.",
        "2. Collect missing evidence for tax IDs, document dates, amounts, and approval trails.",
        "3. Assign each unresolved item to an owner with a target closure date.",
        "4. Generate an audit report after the highest-priority gaps are updated.",
        "5. Re-upload corrected evidence and re-check the dashboard.",
        "",
        f"Current workload: {len(documents)} document(s), {len(risks)} risk flag(s), {len(reports)} report(s).",
    ]

    if critical or warnings:
        lines.extend(["", "Start with these items:"])
        lines.extend(_risk_lines([*critical, *warnings], 5))

    return "\n".join(lines)


def _is_greeting(normalized: str) -> bool:
    return re.search(r"\b(hi|hello|hey)\b", normalized) is not None


def build_workspace_context() -> str:
    """Build compact, evidence-based context for model answers."""
    stored_documents = list_documents()
    eligible_documents = [document for document in stored_documents if is_audit_eligible(document)]
    excluded_documents = [document for document in stored_documents if not is_audit_eligible(document)]
    risks = list_all_risks()
    reports = list_reports()

    lines = [
        "CURRENT PRYSM WORKSPACE SNAPSHOT",
        f"Audit-eligible documents: {len(eligible_documents)}",
        f"Excluded or pending-review files: {len(excluded_documents)}",
        f"Active risk flags: {len(risks)}",
        f"Generated reports: {len(reports)}",
        "",
        "Recent eligible documents:",
    ]
    for document in eligible_documents[-20:]:
        data = document.get("data", {})
        lines.append(
            "- "
            f"{document.get('filename', 'unknown')} | "
            f"type={data.get('document_type', 'unknown')} | "
            f"amount={data.get('amount', 'UNKNOWN')} | "
            f"date={data.get('date', 'UNKNOWN')} | "
            f"gstin={data.get('gstin', 'UNKNOWN')}"
        )

    lines.extend(["", "Priority risks:"])
    for risk in risks[:25]:
        lines.append(
            "- "
            f"{risk.get('severity', 'Info')}: {risk.get('title', risk.get('type', 'Risk'))} | "
            f"source={risk.get('source_document', 'unknown')} | "
            f"action={risk.get('recommendation', 'Review supporting evidence.')}"
        )

    if reports:
        lines.extend(["", "Recent reports:"])
        for report in reports[-5:]:
            lines.append(f"- {report.get('title', report.get('id', 'Report'))}: {report.get('summary', '')}")

    return "\n".join(lines)


def build_system_prompt() -> str:
    return (
        "You are PRYSM Copilot, a capable conversational assistant for audit and compliance work. "
        "Respond naturally and directly, like a high-quality general assistant, while being especially useful "
        "for invoices, audit evidence, controls, risks, and reports. You may answer general questions too. "
        "When discussing the user's PRYSM workspace, use only facts in the supplied snapshot and clearly say "
        "when information is missing. Do not claim that suspicious evidence proves fraud or forgery. "
        "Be concise by default, use bullets only when useful, and provide practical next steps when requested.\n\n"
        + build_workspace_context()
    )


async def generate_copilot_response(request: ChatRequest) -> tuple[str, str, str | None]:
    """Use the configured LLM first, with deterministic guidance as outage fallback."""
    messages = [{"role": "system", "content": build_system_prompt()}]
    for turn in request.history[-20:]:
        content = turn.content.strip()
        if content:
            messages.append({"role": turn.role, "content": content[:4000]})
    messages.append({"role": "user", "content": request.message.strip()[:4000]})

    config = get_llm_model_config()
    try:
        answer, model = await asyncio.to_thread(
            create_chat_completion,
            messages,
            os.getenv("GROQ_API_KEY", ""),
            config["primary_model"],
            config["fallback_model"],
        )
        return answer, "llm", model
    except LLMServiceError:
        return build_copilot_reply(request.message), "fallback", None


def build_copilot_reply(message: str) -> str:
    normalized = message.lower()
    stored_documents = list_documents()
    documents = [document for document in stored_documents if is_audit_eligible(document)]
    risks = list_all_risks()
    reports = list_reports()

    # ── 1. Specific Data Queries (Real Q&A) ───────────────────────
    # Date Gaps
    if "date" in normalized and ("gap" in normalized or "missing" in normalized or "without" in normalized or "no date" in normalized):
        date_gaps = [r for r in risks if r.get("type") == "MISSING_DATE"]
        if not date_gaps:
            return "I scanned your workspace and found no documents with missing dates."
        files = sorted(list(set(r.get("source_document") for r in date_gaps if r.get("source_document"))))
        files_list = "\n".join([f"- {f}" for f in files])
        return (
            f"I found {len(date_gaps)} document(s) with missing date gaps:\n"
            f"{files_list}\n\n"
            "Recommended action: Verify and update the dates on these files."
        )

    # GSTIN Gaps
    if ("gstin" in normalized or "gst" in normalized or "tax id" in normalized or "registration" in normalized) and ("gap" in normalized or "missing" in normalized or "without" in normalized or "no gstin" in normalized):
        gstin_gaps = [r for r in risks if r.get("type") == "MISSING_GSTIN"]
        if not gstin_gaps:
            return "All processed invoices currently have a valid GSTIN."
        files = sorted(list(set(r.get("source_document") for r in gstin_gaps if r.get("source_document"))))
        files_list = "\n".join([f"- {f}" for f in files])
        return (
            f"I found {len(gstin_gaps)} invoice(s) with missing GSTIN/tax gaps:\n"
            f"{files_list}\n\n"
            "Recommended action: Request vendor GSTIN details to ensure compliance."
        )

    # Amount Gaps
    if ("amount" in normalized or "value" in normalized or "price" in normalized) and ("gap" in normalized or "missing" in normalized or "without" in normalized or "no amount" in normalized):
        amount_gaps = [r for r in risks if r.get("type") == "MISSING_AMOUNT"]
        if not amount_gaps:
            return "I found no documents missing monetary amounts."
        files = sorted(list(set(r.get("source_document") for r in amount_gaps if r.get("source_document"))))
        files_list = "\n".join([f"- {f}" for f in files])
        return (
            f"I found {len(amount_gaps)} document(s) with missing monetary values:\n"
            f"{files_list}\n\n"
            "Recommended action: Review these documents and manually enter their invoice totals."
        )

    # High Value Threshold
    if "high value" in normalized or "threshold" in normalized or "above 50" in normalized or "50,000" in normalized or "50000" in normalized:
        high_vals = [r for r in risks if r.get("type") == "HIGH_VALUE_INVOICE"]
        if not high_vals:
            return "No high-value invoices (above the INR 50,000 threshold) were detected."
        files = sorted(list(set(r.get("source_document") for r in high_vals if r.get("source_document"))))
        files_list = "\n".join([f"- {f}" for f in files])
        return (
            f"I detected {len(high_vals)} high-value invoice(s) exceeding the INR 50,000 compliance review threshold:\n"
            f"{files_list}\n\n"
            "Recommended action: Verify senior management approvals and supporting documentation."
        )

    # ── 2. Fallbacks to General Categories ────────────────────────
    if any(term in normalized for term in ["any one", "take one", "pick one", "choose one", "just take"]):
        document = _select_document_for_review(documents)
        if not document:
            return "No uploaded documents are available to review yet."
        return _format_single_document_review(document)

    if any(term in normalized for term in ["readiness", "gap", "gaps", "review", "important", "audit state"]):
        return _format_readiness_review(documents, risks, reports)

    if any(term in normalized for term in ["evidence", "sign-off", "signoff", "collect", "supporting"]):
        return _format_evidence_checklist(documents, risks)

    if any(term in normalized for term in ["next action", "next actions", "recommend", "this week", "plan"]):
        return _format_next_actions(documents, risks, reports)

    if any(term in normalized for term in ["file", "files", "document", "documents", "uploaded", "upload"]):
        return _format_document_list(stored_documents)

    if any(term in normalized for term in ["risk", "risks", "flag", "flags"]):
        return _format_risk_list(risks)

    if any(term in normalized for term in ["report", "reports", "summary"]):
        if reports:
            latest = reports[-1]
            return latest.get("summary") or f"Latest report: {latest.get('title', latest.get('id', 'report'))}"

        return (
            f"Audit snapshot: {len(documents)} document(s) uploaded, "
            f"{len(risks)} risk flag(s), and no generated reports yet."
        )

    if _is_greeting(normalized):
        return "Hi, I am connected to your PRYSM workspace. Ask me about uploaded files, risks, or reports."

    return (
        f"I can see {len(documents)} uploaded document(s), {len(risks)} risk flag(s), "
        f"and {len(reports)} generated report(s). Ask me what files were uploaded, what risks exist, "
        "or to summarize the audit state."
    )

# ── FastAPI app ───────────────────────────────────────────────────
app = FastAPI(
    title="PRYSM API",
    description="Continuous AI Compliance Operating System",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Restore persisted uploads only when a continuing session is explicitly requested."""
    if os.getenv("RESTORE_UPLOADS_ON_STARTUP", "").lower() not in {"1", "true", "yes"}:
        return

    if not os.path.exists(UPLOAD_DIR):
        return

    for entry in os.listdir(UPLOAD_DIR):
        if entry == ".gitkeep":
            continue

        filepath = os.path.join(UPLOAD_DIR, entry)
        if not os.path.isfile(filepath):
            continue

        # Parse document_id and filename (pattern: doc_[a-f0-9]{12}_filename)
        match = re.match(r"^(doc_[a-f0-9]{12})_(.+)$", entry)
        if not match:
            continue

        document_id = match.group(1)
        filename = match.group(2)

        try:
            with open(filepath, "rb") as f:
                content = f.read()

            # Content type fallback
            lower = filename.lower()
            content_type = "application/octet-stream"
            if lower.endswith(".pdf"):
                content_type = "application/pdf"
            elif lower.endswith((".png", ".jpg", ".jpeg")):
                content_type = "image/jpeg"

            # Create document record with file modification time as uploaded_at
            mtime = os.path.getmtime(filepath)
            uploaded_at = datetime.fromtimestamp(mtime, timezone.utc).isoformat().replace("+00:00", "Z")

            doc = build_document_record(document_id, filename, content, content_type, uploaded_at)
            doc["_file_path"] = str(filepath)

            # Store
            save_document(doc)
            save_risks(document_id, doc["risks"])

        except Exception:
            pass

# ── CORS ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════════════════
# HEALTH
# ══════════════════════════════════════════════════════════════════
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "prysm-api", "llm": get_llm_model_config()}


# ══════════════════════════════════════════════════════════════════
# UPLOAD
# ══════════════════════════════════════════════════════════════════
@app.post("/api/v1/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        document_id = f"doc_{uuid.uuid4().hex[:12]}"
        filename = safe_filename(file.filename)
        content_type = file.content_type or "application/octet-stream"
        now = utc_now()

        try:
            content = await file.read()
            filepath = None

            # Save file to disk (optional, for reference)
            try:
                filepath = os.path.join(UPLOAD_DIR, f"{document_id}_{filename}")
                with open(filepath, "wb") as f:
                    f.write(content)
            except Exception:
                pass  # Don't crash if disk write fails

            doc = build_document_record(document_id, filename, content, content_type, now)
            if filepath:
                doc["_file_path"] = str(filepath)

            # Store
            save_document(doc)
            save_risks(document_id, doc["risks"])

            results.append(public_document(doc))

        except Exception:
            # If one file fails, still continue with others
            results.append(failed_upload_document(file))

    return {
        "message": "Documents uploaded",
        "status": "success",
        "documents": results,
    }


# ══════════════════════════════════════════════════════════════════
# DOCUMENTS
# ══════════════════════════════════════════════════════════════════
@app.get("/api/v1/")
async def get_all_documents():
    return {
        "status": "success",
        "documents": [public_document(document) for document in list_documents()],
    }


# ══════════════════════════════════════════════════════════════════
# OVERVIEW / RISKS
# ══════════════════════════════════════════════════════════════════
@app.get("/api/v1/overview")
async def get_overview():
    docs = list_documents()
    audit_docs = [document for document in docs if is_audit_eligible(document)]
    excluded_docs = [
        document for document in docs if document.get("screening", {}).get("decision") == "excluded"
    ]
    review_docs = [
        document for document in docs if document.get("screening", {}).get("decision") == "review_required"
    ]
    all_risks = list_all_risks()

    critical = sum(1 for r in all_risks if r.get("severity") == "Critical")
    warning = sum(1 for r in all_risks if r.get("severity") == "Warning")
    info = sum(1 for r in all_risks if r.get("severity") == "Info")

    return {
        "status": "success",
        "total_documents": len(docs),
        "uploaded_documents": len(audit_docs),
        "excluded_documents": len(excluded_docs),
        "review_documents": len(review_docs),
        "total_risks": len(all_risks),
        "critical_count": critical,
        "warning_count": warning,
        "info_count": info,
        "documents": [public_document(document) for document in docs],
        "risks": all_risks,
    }


@app.get("/api/v1/flags/{document_id}")
async def get_flags(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")

    risks = get_risks(document_id)
    return {
        "status": "success",
        "document_id": document_id,
        "flags": risks,
    }


@app.get("/api/v1/documents/{document_id}/file")
async def get_document_file(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")

    file_path = doc.get("_file_path")
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="The source file is not available in this session.")

    return FileResponse(
        file_path,
        media_type=doc.get("content_type", "application/octet-stream"),
        filename=doc.get("filename", f"{document_id}.bin"),
    )


@app.post("/api/v1/documents/{document_id}/reprocess")
async def reprocess_document(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")

    file_path = doc.get("_file_path")
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="The source file is not available for reprocessing.")

    content = Path(file_path).read_bytes()
    refreshed = build_document_record(
        document_id,
        doc.get("filename", "unknown_file"),
        content,
        doc.get("content_type", "application/octet-stream"),
        doc.get("uploaded_at", utc_now()),
    )
    refreshed["_file_path"] = str(file_path)
    save_document(refreshed)
    save_risks(document_id, refreshed["risks"])
    return public_document(refreshed)


# ══════════════════════════════════════════════════════════════════
# COPILOT
# ══════════════════════════════════════════════════════════════════
@app.post("/api/v1/copilot/chat")
async def copilot_chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    answer, powered_by, model = await generate_copilot_response(request)
    return {
        "status": "success",
        "message": answer,
        "powered_by": powered_by,
        "model": model,
        "documents": [public_document(document) for document in list_documents()],
        "risks": list_all_risks(),
        "reports": list_reports(),
    }


# ══════════════════════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════════════════════
@app.get("/api/v1/reports/")
async def get_all_reports():
    return {
        "status": "success",
        "reports": [public_report(report) for report in list_reports()],
    }


@app.get("/api/v1/reports/{report_id}")
async def get_single_report(report_id: str):
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    return public_report(report)


@app.post("/api/v1/reports/generate")
async def generate_audit_session_report():
    documents = [document for document in list_documents() if is_audit_eligible(document)]
    if not documents:
        raise HTTPException(status_code=409, detail="Upload an eligible audit document before generating a report.")

    report = generate_session_report(documents, list_all_risks(), REPORT_DIR)
    save_report(report)
    return public_report(report)


@app.post("/api/v1/reports/generate/{document_id}")
async def generate_document_report(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    if not is_audit_eligible(doc):
        reason = doc.get("screening_reason", "Document is excluded from audit analysis.")
        raise HTTPException(status_code=409, detail=reason)

    risks = get_risks(document_id)
    report = generate_report(doc, risks)
    save_report(report)

    return public_report(report)


@app.get("/api/v1/reports/{report_id}/download")
async def download_report(report_id: str):
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")

    pdf_path = report.get("_pdf_path")
    if not pdf_path or not Path(pdf_path).exists():
        raise HTTPException(status_code=409, detail="This report does not have a downloadable PDF. Generate a session PDF report.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=report.get("filename", f"{report_id}.pdf"),
    )


# Keep catch-all document routes last so fixed paths like /overview,
# /flags/{document_id}, and /reports/* are not treated as document IDs.
@app.get("/api/v1/{document_id}")
async def get_single_document(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    return public_document(doc)


@app.delete("/api/v1/{document_id}")
async def delete_single_document(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")

    found = delete_document(document_id)
    if not found:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    file_path = doc.get("_file_path")
    if file_path:
        resolved_file = Path(file_path).resolve()
        try:
            resolved_file.relative_to(UPLOAD_DIR.resolve())
            resolved_file.unlink(missing_ok=True)
        except ValueError:
            pass

    return {"status": "success", "message": "Document deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
