"""Screen uploaded files before they enter audit analysis."""

from pathlib import Path


SUPPORTED_DOCUMENT_TYPES = {
    "invoice": "Invoice",
    "audit_report": "Audit Report",
    "bank_statement": "Bank Statement",
    "gst_return": "GST Return",
}

RELEVANT_FILENAME_TERMS = (
    "invoice",
    "audit",
    "statement",
    "ledger",
    "gst",
    "tax",
    "receipt",
)

RELEVANT_TEXT_TERMS = (
    "purchase order",
    "trial balance",
    "general ledger",
    "financial statement",
    "tax return",
    "receipt",
)


def _has_value(value: object) -> bool:
    return value not in (None, "", "UNKNOWN", "NOT_APPLICABLE")


def _extraction_confidence(document_type: str, parsed_data: dict) -> int:
    """Score extraction quality from useful fields rather than a demo constant."""
    expected_fields = {
        "invoice": ("amount", "date", "gstin", "invoice_number", "vendor_name"),
        "audit_report": ("date",),
        "bank_statement": ("amount", "date"),
        "gst_return": ("amount", "date", "gstin"),
    }
    fields = expected_fields.get(document_type, ())
    extracted = sum(_has_value(parsed_data.get(field)) for field in fields)

    if document_type == "invoice":
        return 45 + (extracted * 10)
    if document_type == "audit_report":
        return 70 + (extracted * 20)
    if document_type == "bank_statement":
        return 55 + (extracted * 18)
    if document_type == "gst_return":
        return 50 + (extracted * 15)
    return 0


def screen_document(filename: str, text: str, parsed_data: dict) -> dict:
    """Return the audit eligibility decision and a user-facing explanation."""
    document_type = parsed_data.get("document_type", "unknown")
    if document_type in SUPPORTED_DOCUMENT_TYPES:
        return {
            "decision": "accepted",
            "audit_eligible": True,
            "category": document_type,
            "label": SUPPORTED_DOCUMENT_TYPES[document_type],
            "confidence": _extraction_confidence(document_type, parsed_data),
            "reason": f"Recognized as {SUPPORTED_DOCUMENT_TYPES[document_type].lower()} evidence.",
        }

    lower_filename = Path(filename).name.lower()
    lower_text = text.lower()
    appears_relevant = any(term in lower_filename for term in RELEVANT_FILENAME_TERMS) or any(
        term in lower_text for term in RELEVANT_TEXT_TERMS
    )

    if appears_relevant:
        reason = (
            "This file may be audit evidence, but its contents could not be confidently "
            "classified. Review it before including it in audit analysis."
        )
        if not text.strip():
            reason = (
                "This file looks like audit evidence, but no readable text was extracted. "
                "Review or upload a clearer copy before analysis."
            )
        return {
            "decision": "review_required",
            "audit_eligible": False,
            "category": "unclassified",
            "label": "Needs Review",
            "confidence": 35 if text.strip() else 10,
            "reason": reason,
        }

    reason = "Content does not match a supported audit document or invoice."
    if not text.strip():
        reason = "No readable audit-document content was extracted from this file."
    return {
        "decision": "excluded",
        "audit_eligible": False,
        "category": "unsupported",
        "label": "Excluded",
        "confidence": 0,
        "reason": reason,
    }
