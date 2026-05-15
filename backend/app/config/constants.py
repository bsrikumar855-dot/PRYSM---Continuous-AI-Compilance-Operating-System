"""
Application-wide constants.

NOTE: Prefer using app.core.enums for typed status values.
This module is retained for document type lists and file extension config.
"""

from app.core.enums import (  # noqa: F401 — re-export for backward compat
    ComplianceStatus,
    DocumentType,
    FindingSeverity,
    ReviewState,
)

# --- Supported File Types ---
SUPPORTED_FILE_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".tiff"]

# --- Document Type List (for validation) ---
DOCUMENT_TYPES = [dt.value for dt in DocumentType]
