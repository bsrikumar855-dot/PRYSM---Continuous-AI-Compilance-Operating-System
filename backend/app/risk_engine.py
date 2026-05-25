"""Risk engine for PRYSM backend.

Generates compliance risks based on parsed document data.
"""

import uuid
from datetime import datetime, timezone


def generate_risks(document: dict) -> list:
    """Generate risks based on document parsed data. Never crashes."""
    risks = []
    try:
        data = document.get("data", {})
        doc_type = data.get("document_type", "unknown")
        filename = document.get("filename", "unknown")
        document_id = document.get("document_id") or document.get("id")
        amount_str = data.get("amount", "UNKNOWN")
        gstin = data.get("gstin", "UNKNOWN")
        date = data.get("date", "UNKNOWN")

        if doc_type in ("invoice", "unknown"):
            if gstin == "UNKNOWN":
                risks.append(_make_risk(
                    risk_type="MISSING_GSTIN",
                    severity="Warning",
                    title="Missing GSTIN",
                    message="No valid GSTIN found in this document. GST compliance cannot be verified.",
                    filename=filename,
                    document_id=document_id,
                    recommendation="Request GSTIN from the vendor and update the invoice.",
                ))

            if amount_str == "UNKNOWN":
                risks.append(_make_risk(
                    risk_type="MISSING_AMOUNT",
                    severity="Warning",
                    title="Missing invoice amount",
                    message="Could not extract monetary amount from this document.",
                    filename=filename,
                    document_id=document_id,
                    recommendation="Manually verify the invoice amount and enter it.",
                ))

            if date == "UNKNOWN":
                risks.append(_make_risk(
                    risk_type="MISSING_DATE",
                    severity="Info",
                    title="Missing date",
                    message="No date could be extracted from this document.",
                    filename=filename,
                    document_id=document_id,
                    recommendation="Check the document for a valid date.",
                ))

            if amount_str != "UNKNOWN":
                try:
                    amount = float(amount_str)
                    if amount >= 50000:
                        risks.append(_make_risk(
                            risk_type="HIGH_VALUE_INVOICE",
                            severity="Critical",
                            title="High-value invoice detected",
                            message=(
                                f"This invoice amount (INR {amount:,.2f}) is above "
                                "the review threshold of INR 50,000."
                            ),
                            filename=filename,
                            document_id=document_id,
                            recommendation="Verify supporting documents and approval trail.",
                        ))
                except (ValueError, TypeError):
                    pass

        if doc_type == "audit_report":
            risks.append(_make_risk(
                risk_type="AUDIT_REPORT_UPLOADED",
                severity="Info",
                title="Audit report uploaded",
                message="An audit report has been uploaded for review.",
                filename=filename,
                document_id=document_id,
                recommendation="Review findings and cross-reference with internal records.",
            ))

    except Exception:
        pass

    return risks


def _make_risk(
    risk_type: str,
    severity: str,
    title: str,
    message: str,
    filename: str,
    document_id: str | None,
    recommendation: str,
) -> dict:
    """Create a standardized risk dict."""
    return {
        "id": f"risk_{uuid.uuid4().hex[:10]}",
        "type": risk_type,
        "severity": severity,
        "title": title,
        "message": message,
        "source_document": filename,
        "document_id": document_id,
        "recommendation": recommendation,
        "date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
