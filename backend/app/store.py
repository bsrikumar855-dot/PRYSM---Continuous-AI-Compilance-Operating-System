"""
In-memory storage for PRYSM backend.
No database, no SQLAlchemy. Just dictionaries.
"""

from typing import Optional

# ── In-memory stores ──────────────────────────────────────────────
DOCUMENT_STORE: dict[str, dict] = {}
RISK_STORE: dict[str, list] = {}
REPORT_STORE: dict[str, dict] = {}


# ── Document operations ──────────────────────────────────────────
def save_document(document: dict) -> dict:
    """Save a document to the store. Must contain 'id' key."""
    doc_id = document["id"]
    DOCUMENT_STORE[doc_id] = document
    return document


def list_documents() -> list:
    """Return all documents as a list."""
    return list(DOCUMENT_STORE.values())


def get_document(document_id: str) -> Optional[dict]:
    """Return a single document or None."""
    return DOCUMENT_STORE.get(document_id)


def delete_document(document_id: str) -> bool:
    """Delete a document. Returns True if it existed."""
    if document_id in DOCUMENT_STORE:
        del DOCUMENT_STORE[document_id]
        # Also clean up associated risks
        RISK_STORE.pop(document_id, None)
        return True
    return False


# ── Risk operations ───────────────────────────────────────────────
def save_risks(document_id: str, risks: list) -> None:
    """Save risks for a document."""
    RISK_STORE[document_id] = risks


def get_risks(document_id: str) -> list:
    """Get risks for a specific document."""
    return RISK_STORE.get(document_id, [])


def list_all_risks() -> list:
    """Return all risks across all documents."""
    all_risks = []
    for risks in RISK_STORE.values():
        all_risks.extend(risks)
    return all_risks


# ── Report operations ─────────────────────────────────────────────
def save_report(report: dict) -> dict:
    """Save a report to the store. Must contain 'id' key."""
    report_id = report["id"]
    REPORT_STORE[report_id] = report
    return report


def list_reports() -> list:
    """Return all reports as a list."""
    return list(REPORT_STORE.values())


def get_report(report_id: str) -> Optional[dict]:
    """Return a single report or None."""
    return REPORT_STORE.get(report_id)
