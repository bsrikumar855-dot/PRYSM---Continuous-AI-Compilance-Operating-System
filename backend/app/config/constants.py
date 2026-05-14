"""
Application-wide constants.
"""

# --- Document Types ---
DOCUMENT_TYPES = ["invoice", "gst_return", "bank_statement", "roc_filing", "tds_certificate"]

# --- Compliance Statuses ---
COMPLIANCE_STATUS = {
    "PASS": "pass",
    "FAIL": "fail",
    "WARNING": "warning",
    "PENDING_REVIEW": "pending_review",
    "NOT_APPLICABLE": "not_applicable",
}

# --- Risk Levels ---
RISK_LEVELS = {
    "CRITICAL": "critical",
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
    "INFO": "info",
}

# --- Review Statuses ---
REVIEW_STATUSES = ["pending", "in_progress", "approved", "rejected", "escalated"]

# --- Workflow States ---
WORKFLOW_STATES = [
    "uploaded",
    "ocr_processing",
    "ocr_complete",
    "extracting",
    "extraction_complete",
    "compliance_checking",
    "compliance_complete",
    "risk_scoring",
    "risk_complete",
    "pending_review",
    "reviewed",
    "report_generating",
    "complete",
    "error",
]

# --- Supported File Types ---
SUPPORTED_FILE_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".tiff"]
