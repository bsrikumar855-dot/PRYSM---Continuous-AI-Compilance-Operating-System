"""
PRYSM Centralized Enum System
==============================
All system-wide enumerations live here. No magic strings in business logic.

Usage:
    from app.core.enums import DocumentStatus, FindingSeverity
    document.status = DocumentStatus.UPLOADED
"""

from enum import StrEnum


# =============================================================================
# Document Processing
# =============================================================================

class DocumentStatus(StrEnum):
    """Lifecycle states for a document in the processing pipeline."""
    UPLOADED = "uploaded"
    OCR_PROCESSING = "ocr_processing"
    OCR_COMPLETE = "ocr_complete"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    VALIDATING = "validating"
    ANALYZING = "analyzing"
    REVIEW_PENDING = "review_pending"
    REPORT_READY = "report_ready"
    COMPLETE = "complete"
    FAILED = "failed"


class DocumentType(StrEnum):
    """Types of financial/compliance documents handled by PRYSM."""
    INVOICE = "invoice"
    GST_RETURN = "gst_return"
    BANK_STATEMENT = "bank_statement"
    ROC_FILING = "roc_filing"
    TDS_CERTIFICATE = "tds_certificate"


# =============================================================================
# Risk & Compliance
# =============================================================================

class FindingSeverity(StrEnum):
    """Severity levels for compliance findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(StrEnum):
    """Status of an individual compliance finding."""
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    AWAITING_EVIDENCE = "awaiting_evidence"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    ACCEPTED_RISK = "accepted_risk"


class ComplianceStatus(StrEnum):
    """Result status for a compliance rule check."""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    PENDING_REVIEW = "pending_review"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


class RiskLevel(StrEnum):
    """Risk classification levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# =============================================================================
# Human Review Workflow
# =============================================================================

class ReviewState(StrEnum):
    """States for human review tasks."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class ReviewPriority(StrEnum):
    """Priority levels for review tasks."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# =============================================================================
# Workflow & Processing
# =============================================================================

class WorkflowStage(StrEnum):
    """High-level workflow pipeline stages."""
    INGESTION = "ingestion"
    OCR = "ocr"
    EXTRACTION = "extraction"
    VALIDATION = "validation"
    COMPLIANCE = "compliance"
    RISK_SCORING = "risk_scoring"
    REVIEW = "review"
    REPORTING = "reporting"
    COMPLETE = "complete"


class ProcessingState(StrEnum):
    """Generic processing state for any async operation."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# =============================================================================
# Agents
# =============================================================================

class AgentType(StrEnum):
    """Types of AI agents in the PRYSM pipeline."""
    EXTRACTION = "extraction"
    COMPLIANCE = "compliance"
    RISK = "risk"
    EVIDENCE = "evidence"
    REPORTING = "reporting"
    COPILOT = "copilot"


# =============================================================================
# Evidence Graph
# =============================================================================

class RelationshipType(StrEnum):
    """Types of relationships between compliance evidence entities."""
    MATCHES = "matches"
    DISCREPANT = "discrepant"
    MISSING = "missing"
    REFERENCES = "references"
    RECONCILED = "reconciled"
    DUPLICATE = "duplicate"


class EvidenceEntityType(StrEnum):
    """Types of entities that can participate in evidence relationships."""
    INVOICE = "invoice"
    GST_FILING = "gst_filing"
    BANK_TRANSACTION = "bank_transaction"
    VENDOR = "vendor"
    ROC_RECORD = "roc_record"
    TDS_CERTIFICATE = "tds_certificate"


# =============================================================================
# Audit
# =============================================================================

class AuditAction(StrEnum):
    """Actions tracked in the audit log."""
    DOCUMENT_UPLOADED = "document_uploaded"
    EXTRACTION_STARTED = "extraction_started"
    EXTRACTION_COMPLETED = "extraction_completed"
    ANALYSIS_STARTED = "analysis_started"
    ANALYSIS_COMPLETED = "analysis_completed"
    RISK_DETECTED = "risk_detected"
    REVIEW_CREATED = "review_created"
    REVIEW_APPROVED = "review_approved"
    REVIEW_REJECTED = "review_rejected"
    REVIEW_ESCALATED = "review_escalated"
    REPORT_GENERATED = "report_generated"
    STATUS_CHANGED = "status_changed"


# =============================================================================
# Compliance Domains
# =============================================================================

class ComplianceDomain(StrEnum):
    """Regulatory/compliance domains for rule classification."""
    GST = "gst"
    INVOICE = "invoice"
    BANK = "bank"
    STATUTORY = "statutory"
    ROC = "roc"
    TDS = "tds"


# =============================================================================
# Severity Weight Map (for risk scoring)
# =============================================================================

SEVERITY_WEIGHT: dict[FindingSeverity, int] = {
    FindingSeverity.CRITICAL: 100,
    FindingSeverity.HIGH: 75,
    FindingSeverity.MEDIUM: 50,
    FindingSeverity.LOW: 25,
    FindingSeverity.INFO: 0,
}
