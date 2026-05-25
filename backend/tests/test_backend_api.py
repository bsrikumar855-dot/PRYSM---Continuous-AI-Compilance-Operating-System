"""Smoke tests for the simplified PRYSM backend."""

import asyncio
import shutil
import uuid
import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.llm_client import LLMServiceError
from app.main import app
from app.store import DOCUMENT_STORE, REPORT_STORE, RISK_STORE


client = TestClient(app)
main_module = importlib.import_module("app.main")


@pytest.fixture(autouse=True)
def isolate_test_session(monkeypatch):
    upload_dir = Path(__file__).parent / f".uploads-{uuid.uuid4().hex}"
    upload_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(main_module, "UPLOAD_DIR", upload_dir)
    DOCUMENT_STORE.clear()
    RISK_STORE.clear()
    REPORT_STORE.clear()

    yield

    DOCUMENT_STORE.clear()
    RISK_STORE.clear()
    REPORT_STORE.clear()
    shutil.rmtree(upload_dir, ignore_errors=True)


def force_copilot_fallback(monkeypatch):
    def unavailable(*args, **kwargs):
        raise LLMServiceError("model unavailable during fallback test")

    monkeypatch.setattr("app.main.create_chat_completion", unavailable)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_returns_document_contract_and_parsed_text_fields():
    response = client.post(
        "/api/v1/upload",
        files={
            "files": (
                "invoice.txt",
                b"Seller: Acme Pvt Ltd\nInvoice No: INV-001\nGSTIN: 29ABCDE1234F1Z5\nTotal INR 12345\nDate: 21/05/2026",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200
    payload = response.json()
    document = payload["documents"][0]

    assert payload["status"] == "success"
    assert document["id"].startswith("doc_")
    assert document["document_id"] == document["id"]
    assert document["filename"] == "invoice.txt"
    assert document["status"] == "uploaded"
    assert document["content_type"] == "text/plain"
    assert document["size_bytes"] > 0
    assert document["uploaded_at"].endswith("Z")
    assert document["data"]["document_type"] == "invoice"
    assert document["data"]["amount"] == "12345"
    assert document["data"]["gstin"] == "29ABCDE1234F1Z5"
    assert document["data"]["invoice_number"] == "INV-001"
    assert document["screening"]["confidence"] == 95


def test_extraction_confidence_reflects_missing_fields_and_avoids_generic_invoice_match():
    incomplete = client.post(
        "/api/v1/upload",
        files={"files": ("invoice.txt", b"Invoice No: INV-002\nTotal INR 5000", "text/plain")},
    ).json()["documents"][0]
    filing = client.post(
        "/api/v1/upload",
        files={"files": ("annual-filing.txt", b"Annual company filing mentioning invoice controls only.", "text/plain")},
    ).json()["documents"][0]

    assert incomplete["screening"]["confidence"] == 65
    assert filing["data"]["document_type"] == "unknown"
    assert filing["screening"]["audit_eligible"] is False


def test_uploaded_source_can_be_viewed_reprocessed_and_deleted():
    upload = client.post(
        "/api/v1/upload",
        files={"files": ("source-invoice.txt", b"Invoice No: SRC-1\nTotal INR 1250", "text/plain")},
    )
    document = upload.json()["documents"][0]
    document_id = document["document_id"]
    stored_file = next(main_module.UPLOAD_DIR.glob(f"{document_id}_*"))

    source = client.get(f"/api/v1/documents/{document_id}/file")
    refreshed = client.post(f"/api/v1/documents/{document_id}/reprocess")
    deleted = client.delete(f"/api/v1/{document_id}")

    assert "_file_path" not in document
    assert source.status_code == 200
    assert source.content.startswith(b"Invoice No")
    assert refreshed.status_code == 200
    assert refreshed.json()["document_id"] == document_id
    assert "_file_path" not in refreshed.json()
    assert deleted.status_code == 200
    assert not stored_file.exists()


def test_fresh_start_does_not_restore_persisted_uploads_by_default(monkeypatch):
    client.post(
        "/api/v1/upload",
        files={"files": ("persisted-invoice.txt", b"Invoice No: OLD-1\nTotal INR 1250", "text/plain")},
    )
    DOCUMENT_STORE.clear()
    RISK_STORE.clear()
    monkeypatch.delenv("RESTORE_UPLOADS_ON_STARTUP", raising=False)

    asyncio.run(main_module.startup_event())

    assert client.get("/api/v1/").json()["documents"] == []


def test_uploaded_document_works_with_followup_routes():
    upload = client.post(
        "/api/v1/upload",
        files={"files": ("audit.txt", b"Audit report for financial year 2026", "text/plain")},
    )
    document_id = upload.json()["documents"][0]["document_id"]

    detail = client.get(f"/api/v1/{document_id}")
    flags = client.get(f"/api/v1/flags/{document_id}")
    report = client.post(f"/api/v1/reports/generate/{document_id}")

    assert detail.status_code == 200
    assert detail.json()["document_id"] == document_id
    assert flags.status_code == 200
    assert flags.json()["status"] == "success"
    assert flags.json()["document_id"] == document_id
    assert report.status_code == 200
    assert report.json()["report_id"].startswith("report_")
    assert report.json()["document_id"] == document_id


def test_unrelated_file_is_excluded_from_audit_and_reports():
    upload = client.post(
        "/api/v1/upload",
        files={"files": ("team-notes.txt", b"Birthday lunch plans and presentation ideas", "text/plain")},
    )
    document = upload.json()["documents"][0]
    document_id = document["document_id"]

    flags = client.get(f"/api/v1/flags/{document_id}")
    report = client.post(f"/api/v1/reports/generate/{document_id}")

    assert upload.status_code == 200
    assert document["status"] == "excluded"
    assert document["screening"]["audit_eligible"] is False
    assert "does not match" in document["screening_reason"]
    assert flags.json()["flags"] == []
    assert report.status_code == 409


def test_unreadable_invoice_like_file_requires_review_without_generating_risks():
    upload = client.post(
        "/api/v1/upload",
        files={"files": ("invoice-scan.pdf", b"not a readable pdf", "application/pdf")},
    )
    document = upload.json()["documents"][0]

    assert document["status"] == "review_required"
    assert document["screening"]["audit_eligible"] is False
    assert document["risks"] == []
    assert "clearer copy" in document["screening_reason"]


def test_generate_session_report_creates_downloadable_pdf_and_latex_source(monkeypatch):
    output_dir = Path(__file__).parent / f".generated-report-{uuid.uuid4().hex}"
    monkeypatch.setattr("app.main.REPORT_DIR", output_dir)
    try:
        client.post(
            "/api/v1/upload",
            files={"files": ("session-invoice.txt", b"Invoice No: PDF-001\nTotal INR 75000", "text/plain")},
        )

        generated = client.post("/api/v1/reports/generate")
        report = generated.json()
        download = client.get(f"/api/v1/reports/{report['id']}/download")
        latex_files = list(output_dir.glob("*.tex"))

        assert generated.status_code == 200
        assert report["title"] == "PRYSM Audit Evidence Review Report"
        assert report["metrics"]["evidenceQualityScore"] == 65
        assert report["metrics"]["readinessScore"] < 100
        assert report["pdf_generation"] in ("latex", "latex-source-with-pdf-fallback")
        assert download.status_code == 200
        assert download.headers["content-type"] == "application/pdf"
        assert download.content.startswith(b"%PDF")
        assert len(latex_files) == 1
        assert r"\definecolor{prysmgold}" in latex_files[0].read_text(encoding="utf-8")
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)


def test_copilot_can_answer_uploaded_files(monkeypatch):
    force_copilot_fallback(monkeypatch)
    client.post(
        "/api/v1/upload",
        files={"files": ("copilot-invoice.txt", b"Invoice No: CHAT-001\nTotal INR 100", "text/plain")},
    )

    response = client.post("/api/v1/copilot/chat", json={"message": "what files have I uploaded?"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert "Uploaded files:" in payload["message"]
    assert "copilot-invoice.txt" in payload["message"]


def test_copilot_reviews_readiness_and_can_pick_one_document(monkeypatch):
    force_copilot_fallback(monkeypatch)
    client.post(
        "/api/v1/upload",
        files={"files": ("readiness-invoice.txt", b"Invoice No: READY-001\nTotal INR 75000", "text/plain")},
    )

    readiness = client.post(
        "/api/v1/copilot/chat",
        json={"message": "Review our audit readiness and call out the most important gaps."},
    )
    picked = client.post("/api/v1/copilot/chat", json={"message": "just take any one"})

    assert readiness.status_code == 200
    assert "Audit readiness review:" in readiness.json()["message"]
    assert "Most important gaps:" in readiness.json()["message"]
    assert picked.status_code == 200
    assert "I picked" in picked.json()["message"]
    assert "Quick review:" in picked.json()["message"]


def test_copilot_handles_next_actions_and_evidence_prompts(monkeypatch):
    force_copilot_fallback(monkeypatch)
    client.post(
        "/api/v1/upload",
        files={"files": ("evidence-invoice.txt", b"Invoice No: EVID-001\nTotal INR 75000", "text/plain")},
    )

    next_actions = client.post(
        "/api/v1/copilot/chat",
        json={"message": "Recommend the next compliance actions for this week."},
    )
    evidence = client.post(
        "/api/v1/copilot/chat",
        json={"message": "What evidence should I collect before sign-off?"},
    )

    assert next_actions.status_code == 200
    assert "Recommended compliance actions for this week:" in next_actions.json()["message"]
    assert "Hi, I am connected" not in next_actions.json()["message"]
    assert evidence.status_code == 200
    assert "Evidence to collect before sign-off:" in evidence.json()["message"]


def test_copilot_uses_model_with_history_and_workspace_context(monkeypatch):
    captured = {}

    def complete(messages, api_key, primary_model, fallback_model):
        captured["messages"] = messages
        captured["primary_model"] = primary_model
        return "A conversational, workspace-aware answer.", primary_model

    monkeypatch.setattr("app.main.create_chat_completion", complete)

    response = client.post(
        "/api/v1/copilot/chat",
        json={
            "message": "Now turn that into a short management update.",
            "history": [
                {"role": "user", "content": "What risks do we have?"},
                {"role": "assistant", "content": "There are open risk flags."},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "A conversational, workspace-aware answer."
    assert payload["powered_by"] == "llm"
    assert payload["model"] == captured["primary_model"]
    assert "CURRENT PRYSM WORKSPACE SNAPSHOT" in captured["messages"][0]["content"]
    assert captured["messages"][-2]["content"] == "There are open risk flags."
    assert captured["messages"][-1]["content"] == "Now turn that into a short management update."
