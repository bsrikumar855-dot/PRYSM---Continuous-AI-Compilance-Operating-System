"""Generate structured and downloadable PRYSM audit reports."""

import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

import fitz


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def generate_report(document: dict, risks: list) -> dict:
    """Generate an audit readiness report for a document."""
    report_id = f"report_{uuid.uuid4().hex[:10]}"
    doc_id = document.get("id", "unknown")
    filename = document.get("filename", "unknown")
    now = _utc_now()

    risk_count = len(risks)
    critical = sum(1 for risk in risks if risk.get("severity") == "Critical")
    warnings = sum(1 for risk in risks if risk.get("severity") == "Warning")

    if risk_count == 0:
        summary = f"Audit readiness report for {filename}. No risks detected."
    else:
        summary = (
            f"Audit readiness report for {filename}. "
            f"Found {risk_count} risk(s): {critical} critical, {warnings} warning(s)."
        )

    return {
        "id": report_id,
        "report_id": report_id,
        "document_id": doc_id,
        "filename": filename,
        "title": f"Audit Report - {filename}",
        "status": "generated",
        "summary": summary,
        "risk_count": risk_count,
        "generated_at": now,
        "date": now,
        "metrics": {
            "readinessScore": max(0, 100 - (critical * 20) - (warnings * 5)),
            "readinessTotal": 100,
            "criticalRisks": critical,
            "complianceGaps": warnings,
        },
        "topRisks": [
            {
                "id": risk.get("id"),
                "issue": risk.get("title"),
                "entity": risk.get("source_document"),
                "impact": risk.get("message"),
            }
            for risk in risks[:5]
        ],
        "risks": risks,
    }


def _latex_escape(value: object) -> str:
    text = str(value or "")
    for old, new in (
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ):
        text = text.replace(old, new)
    return text


def _actionable_risks(risks: list[dict]) -> list[dict]:
    return [risk for risk in risks if risk.get("severity") in {"Critical", "Warning"}]


def _document_inventory(documents: list[dict]) -> list[dict]:
    """Group duplicate submissions for a concise evidence register."""
    inventory: dict[tuple[str, str, int], dict] = {}
    for document in documents:
        filename = str(document.get("filename", "Unknown"))
        doc_type = str(document.get("data", {}).get("document_type", "unknown"))
        confidence = int(document.get("screening", {}).get("confidence", 0) or 0)
        key = (filename, doc_type, confidence)
        if key not in inventory:
            inventory[key] = {
                "filename": filename,
                "document_type": doc_type,
                "confidence": confidence,
                "copies": 0,
            }
        inventory[key]["copies"] += 1
    return list(inventory.values())


def _session_metrics(documents: list[dict], risks: list[dict]) -> dict:
    critical = sum(1 for risk in risks if risk.get("severity") == "Critical")
    warnings = sum(1 for risk in risks if risk.get("severity") == "Warning")
    info = sum(1 for risk in risks if risk.get("severity") == "Info")
    confidences = [int(document.get("screening", {}).get("confidence", 0) or 0) for document in documents]
    evidence_quality = round(sum(confidences) / len(confidences)) if confidences else 0
    readiness_score = max(0, evidence_quality - (critical * 20) - (warnings * 5))
    return {
        "readinessScore": readiness_score,
        "readinessTotal": 100,
        "evidenceQualityScore": evidence_quality,
        "criticalRisks": critical,
        "complianceGaps": warnings,
        "informationFlags": info,
        "documentsReviewed": len(documents),
        "uniqueDocuments": len(_document_inventory(documents)),
    }


def _build_latex(report: dict, documents: list[dict], risks: list[dict]) -> str:
    metrics = report["metrics"]
    actionable_risks = _actionable_risks(risks)
    inventory = _document_inventory(documents)
    risk_rows = "\n".join(
        r"\textbf{" + _latex_escape(risk.get("severity", "Info")) + "} & "
        + _latex_escape(risk.get("title", risk.get("type", "Risk"))) + " & "
        + _latex_escape(risk.get("source_document", "Unknown")) + r" \\ \hline"
        for risk in actionable_risks[:15]
    ) or r"\multicolumn{3}{l}{No actionable exceptions identified by automated checks.} \\ \hline"
    document_rows = "\n".join(
        _latex_escape(item["filename"]) + " & "
        + _latex_escape(item["document_type"].replace("_", " ").title()) + " & "
        + str(item["confidence"]) + r"\% & " + str(item["copies"]) + r" \\ \hline"
        for item in inventory
    ) or r"\multicolumn{3}{l}{No eligible documents found.} \\ \hline"

    return rf"""\documentclass[11pt,a4paper]{{article}}
\usepackage[margin=0.72in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern,xcolor,colortbl,tabularx,longtable,array,fancyhdr,titlesec}}
\definecolor{{prysmgold}}{{HTML}}{{D4A830}}
\definecolor{{prysmdark}}{{HTML}}{{111318}}
\definecolor{{prysmslate}}{{HTML}}{{39424E}}
\definecolor{{prysmlight}}{{HTML}}{{F7F3E8}}
\definecolor{{critical}}{{HTML}}{{A11D33}}
\definecolor{{success}}{{HTML}}{{087F5B}}
\pagestyle{{fancy}}
\fancyhf{{}}
\lhead{{\textcolor{{prysmgold}}{{\textbf{{PRYSM}}}}}}
\rhead{{\textcolor{{prysmslate}}{{Audit Intelligence}}}}
\cfoot{{\textcolor{{prysmslate}}{{\thepage}}}}
\titleformat{{\section}}{{\large\bfseries\color{{prysmdark}}}}{{}}{{0pt}}{{}}
\begin{{document}}
\color{{prysmdark}}
\noindent\colorbox{{prysmdark}}{{\parbox[c][2.25cm][c]{{\dimexpr\textwidth-2\fboxsep}}{{\color{{white}}\Huge\textbf{{PRYSM}}\\[-1mm]\large\textcolor{{prysmgold}}{{Audit Readiness Session Report}}}}}}

\vspace{{0.45cm}}
\noindent\textcolor{{prysmslate}}{{Generated: {_latex_escape(report["date"])}}}\hfill
\textcolor{{prysmslate}}{{Report ID: {_latex_escape(report["id"])}}}

\section*{{Executive Summary}}
\colorbox{{prysmlight}}{{\parbox{{\dimexpr\textwidth-2\fboxsep}}{{\vspace{{2mm}}{_latex_escape(report["summary"])}\vspace{{2mm}}}}}}

\section*{{Readiness Overview}}
\renewcommand{{\arraystretch}}{{1.7}}
\begin{{tabularx}}{{\textwidth}}{{|>{{\columncolor{{prysmlight}}}}X|>{{\centering\arraybackslash}}X|>{{\centering\arraybackslash}}X|>{{\centering\arraybackslash}}X|}}
\hline
\textbf{{Documents Reviewed}} & \textbf{{Evidence Quality}} & \textbf{{Critical Risks}} & \textbf{{Warnings}} \\ \hline
{metrics["documentsReviewed"]} & \textcolor{{success}}{{\textbf{{{metrics["evidenceQualityScore"]}/100}}}} & \textcolor{{critical}}{{\textbf{{{metrics["criticalRisks"]}}}}} & \textbf{{{metrics["complianceGaps"]}}} \\ \hline
\end{{tabularx}}

\section*{{Actionable Exceptions}}
\rowcolors{{2}}{{prysmlight}}{{white}}
\begin{{tabularx}}{{\textwidth}}{{|p{{2.2cm}}|X|p{{4.1cm}}|}}
\hline
\rowcolor{{prysmgold!25}}\textbf{{Severity}} & \textbf{{Finding}} & \textbf{{Source Document}} \\ \hline
{risk_rows}
\end{{tabularx}}

\newpage
\section*{{Evidence Register}}
\begin{{longtable}}{{|p{{7cm}}|p{{3.2cm}}|p{{2.2cm}}|p{{1.2cm}}|}}
\hline
\rowcolor{{prysmgold!25}}\textbf{{Filename}} & \textbf{{Classification}} & \textbf{{Confidence}} & \textbf{{Count}} \\ \hline
\endfirsthead
\hline
\rowcolor{{prysmgold!25}}\textbf{{Filename}} & \textbf{{Classification}} & \textbf{{Confidence}} & \textbf{{Count}} \\ \hline
\endhead
{document_rows}
\end{{longtable}}

\vfill
\noindent\textcolor{{prysmslate}}{{This report is generated from extracted audit evidence. Material findings should be verified against source documents before sign-off.}}
\end{{document}}
"""


def _render_fallback_pdf(report: dict, documents: list[dict], risks: list[dict], pdf_path: Path) -> None:
    """Render the branded report immediately when a TeX compiler is unavailable."""
    metrics = report["metrics"]
    actionable_risks = _actionable_risks(risks)
    inventory = _document_inventory(documents)
    document = fitz.open()
    dark = (0.07, 0.08, 0.10)
    gold = (0.83, 0.66, 0.19)
    slate = (0.25, 0.30, 0.36)
    pale = (0.97, 0.95, 0.90)
    red = (0.63, 0.11, 0.20)
    green = (0.03, 0.50, 0.36)

    def text(page: fitz.Page, x: float, y: float, value: str, size: float = 9, color=dark, font="helv"):
        page.insert_text((x, y), value, fontsize=size, fontname=font, color=color)

    def add_register_page() -> fitz.Page:
        page = document.new_page(width=595, height=842)
        page.draw_rect(fitz.Rect(0, 0, 595, 76), color=dark, fill=dark)
        text(page, 42, 42, "PRYSM", 18, (1, 1, 1), "hebo")
        text(page, 42, 63, "Audit Evidence Register", 10, gold, "hebo")
        return page

    page = document.new_page(width=595, height=842)
    page.draw_rect(fitz.Rect(0, 0, 595, 112), color=dark, fill=dark)
    text(page, 42, 50, "PRYSM", 28, (1, 1, 1), "hebo")
    text(page, 42, 77, "Audit Evidence Review Report", 16, gold, "hebo")
    text(page, 42, 132, f"Generated: {report['date'][:10]}", 9, slate)
    text(page, 390, 132, f"Report ID: {report['id']}", 9, slate)
    text(page, 42, 165, "Executive Summary", 14, dark, "hebo")
    page.draw_rect(fitz.Rect(42, 180, 553, 237), color=pale, fill=pale)
    page.insert_textbox(fitz.Rect(55, 192, 540, 225), report["summary"], fontsize=9, fontname="helv", color=slate)
    text(page, 42, 269, "Assessment Overview", 14, dark, "hebo")

    cards = [
        ("Documents Reviewed", str(metrics["documentsReviewed"]), dark),
        ("Evidence Quality", f"{metrics['evidenceQualityScore']}/100", green),
        ("Critical Risks", str(metrics["criticalRisks"]), red),
        ("Warnings", str(metrics["complianceGaps"]), gold),
    ]
    for index, (label, value, value_color) in enumerate(cards):
        left = 42 + index * 130
        page.draw_rect(fitz.Rect(left, 286, left + 118, 343), color=(0.90, 0.89, 0.85), fill=pale)
        text(page, left + 9, 305, label, 8, slate, "hebo")
        text(page, left + 9, 330, value, 18, value_color, "hebo")

    text(page, 42, 378, "Actionable Exceptions", 14, dark, "hebo")
    top = 394
    for risk in actionable_risks[:7]:
        severity = str(risk.get("severity", "Info"))
        title = str(risk.get("title", risk.get("type", "Risk")))[:48]
        source = str(risk.get("source_document", "Unknown"))[:36]
        page.draw_rect(fitz.Rect(42, top, 553, top + 31), color=(0.92, 0.91, 0.88), fill=pale if top % 2 else (1, 1, 1))
        text(page, 51, top + 19, severity, 8, red if severity == "Critical" else gold, "hebo")
        text(page, 128, top + 19, title, 8, dark)
        text(page, 363, top + 19, source, 8, slate)
        top += 31
    if not actionable_risks:
        page.draw_rect(fitz.Rect(42, top, 553, top + 48), color=(0.86, 0.95, 0.91), fill=(0.95, 0.99, 0.97))
        text(page, 55, top + 20, "No actionable exceptions identified by automated checks.", 9, green, "hebo")
        text(page, 55, top + 36, "Informational evidence records remain subject to reviewer sign-off.", 8, slate)

    text(page, 42, 690, "Basis of Assessment", 14, dark, "hebo")
    basis = (
        "Readiness reflects extraction quality and identified exceptions. "
        "This automated review does not replace source-document verification or professional judgement."
    )
    page.insert_textbox(fitz.Rect(42, 708, 553, 744), basis, fontsize=9, fontname="helv", color=slate)

    register_page = add_register_page()
    text(register_page, 42, 112, "Evidence Register", 15, dark, "hebo")
    text(register_page, 42, 132, f"{len(documents)} submission(s), grouped into {len(inventory)} source record(s).", 9, slate)
    top = 154

    def draw_register_header(target: fitz.Page, y: float) -> None:
        target.draw_rect(fitz.Rect(42, y, 553, y + 28), color=(0.90, 0.89, 0.85), fill=pale)
        text(target, 51, y + 18, "Source Document", 8, slate, "hebo")
        text(target, 350, y + 18, "Classification", 8, slate, "hebo")
        text(target, 464, y + 18, "Confidence", 8, slate, "hebo")
        text(target, 530, y + 18, "Qty", 8, slate, "hebo")

    draw_register_header(register_page, top)
    top += 28
    for item in inventory:
        if top > 760:
            register_page = add_register_page()
            text(register_page, 42, 112, "Evidence Register (continued)", 15, dark, "hebo")
            top = 144
            draw_register_header(register_page, top)
            top += 28
        register_page.draw_rect(fitz.Rect(42, top, 553, top + 28), color=(0.92, 0.91, 0.88), fill=pale if int(top) % 2 else (1, 1, 1))
        text(register_page, 51, top + 18, item["filename"][:50], 8, dark)
        text(register_page, 350, top + 18, item["document_type"].replace("_", " ").title()[:18], 8, slate)
        text(register_page, 474, top + 18, f"{item['confidence']}%", 8, slate)
        text(register_page, 535, top + 18, str(item["copies"]), 8, slate)
        top += 28

    total_pages = document.page_count
    for page_number, report_page in enumerate(document, start=1):
        text(report_page, 42, 809, "Verify material findings against source evidence before sign-off.", 8, slate)
        text(report_page, 523, 809, f"{page_number}/{total_pages}", 8, slate)

    document.save(pdf_path)
    document.close()


def generate_session_report(documents: list[dict], risks: list[dict], output_dir: Path) -> dict:
    """Create a downloadable, branded report for the current audit session."""
    report_id = f"report_{uuid.uuid4().hex[:10]}"
    now = _utc_now()
    metrics = _session_metrics(documents, risks)
    actionable_risks = _actionable_risks(risks)
    report = {
        "id": report_id,
        "report_id": report_id,
        "filename": f"{report_id}_prysm_audit_session.pdf",
        "title": "PRYSM Audit Evidence Review Report",
        "status": "generated",
        "generatedBy": "PRYSM Audit Intelligence",
        "preparedFor": "Audit Review Team",
        "period": now[:10],
        "summary": (
            f"Automated review covered {metrics['documentsReviewed']} eligible submission(s) "
            f"across {metrics['uniqueDocuments']} grouped source record(s). Evidence quality scored "
            f"{metrics['evidenceQualityScore']}/100. Identified {len(actionable_risks)} actionable "
            f"exception(s): {metrics['criticalRisks']} critical and {metrics['complianceGaps']} warning."
        ),
        "risk_count": len(actionable_risks),
        "information_count": metrics["informationFlags"],
        "generated_at": now,
        "date": now,
        "metrics": metrics,
        "topRisks": [
            {
                "id": risk.get("id"),
                "issue": risk.get("title"),
                "entity": risk.get("source_document"),
                "impact": risk.get("message"),
            }
            for risk in actionable_risks[:8]
        ],
        "risks": risks,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    tex_path = output_dir / f"{report_id}_prysm_audit_session.tex"
    pdf_path = output_dir / report["filename"]
    tex_path.write_text(_build_latex(report, documents, risks), encoding="utf-8")

    compiler = shutil.which("xelatex") or shutil.which("pdflatex")
    generation_method = "latex"
    if compiler:
        result = subprocess.run(
            [compiler, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=output_dir,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        generated_pdf = output_dir / f"{tex_path.stem}.pdf"
        if result.returncode == 0 and generated_pdf.exists():
            if generated_pdf != pdf_path:
                generated_pdf.replace(pdf_path)
        else:
            generation_method = "latex-source-with-pdf-fallback"
            _render_fallback_pdf(report, documents, risks, pdf_path)
    else:
        generation_method = "latex-source-with-pdf-fallback"
        _render_fallback_pdf(report, documents, risks, pdf_path)

    report["_pdf_path"] = str(pdf_path)
    report["_tex_path"] = str(tex_path)
    report["pdf_generation"] = generation_method
    report["downloadUrl"] = f"/api/v1/reports/{report_id}/download"
    return report
