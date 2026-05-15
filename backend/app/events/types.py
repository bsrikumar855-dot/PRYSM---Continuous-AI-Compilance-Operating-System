"""
PRYSM Domain Event Types
==========================
Typed event classes for every significant domain action.
Each event is a frozen dataclass for immutability and audit safety.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


# =============================================================================
# Base Event
# =============================================================================

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all PRYSM domain events."""

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        compare=False,
    )

    def to_dict(self) -> dict[str, Any]:
        """Serialize event to a dict for logging/persistence."""
        data = asdict(self)
        data["event_type"] = type(self).__name__
        # Convert datetime to ISO string for JSON serialization
        if isinstance(data.get("timestamp"), datetime):
            data["timestamp"] = data["timestamp"].isoformat()
        return data


# =============================================================================
# Document Lifecycle Events
# =============================================================================

@dataclass(frozen=True)
class DocumentUploaded(DomainEvent):
    """Fired when a new document is uploaded to the system."""
    doc_id: str = ""
    filename: str = ""
    content_type: str = ""
    file_hash: str = ""


@dataclass(frozen=True)
class DocumentStatusChanged(DomainEvent):
    """Fired when a document transitions to a new processing state."""
    doc_id: str = ""
    from_status: str = ""
    to_status: str = ""
    triggered_by: str = "system"


# =============================================================================
# Extraction Events
# =============================================================================

@dataclass(frozen=True)
class ExtractionStarted(DomainEvent):
    """Fired when entity extraction begins for a document."""
    doc_id: str = ""


@dataclass(frozen=True)
class ExtractionCompleted(DomainEvent):
    """Fired when entity extraction finishes successfully."""
    doc_id: str = ""
    entity_count: int = 0
    confidence: float = 0.0


@dataclass(frozen=True)
class ExtractionFailed(DomainEvent):
    """Fired when entity extraction fails."""
    doc_id: str = ""
    error: str = ""


# =============================================================================
# Compliance & Risk Events
# =============================================================================

@dataclass(frozen=True)
class AnalysisCompleted(DomainEvent):
    """Fired when compliance analysis finishes for a document."""
    doc_id: str = ""
    finding_count: int = 0
    critical_count: int = 0


@dataclass(frozen=True)
class RiskDetected(DomainEvent):
    """Fired when a new risk finding is created."""
    doc_id: str = ""
    rule_id: str = ""
    severity: str = ""
    risk_score: int = 0


# =============================================================================
# Review Events
# =============================================================================

@dataclass(frozen=True)
class ReviewCreated(DomainEvent):
    """Fired when a review task is created."""
    task_id: str = ""
    doc_id: str = ""
    priority: str = "medium"


@dataclass(frozen=True)
class ReviewEscalated(DomainEvent):
    """Fired when a review task is escalated."""
    task_id: str = ""
    doc_id: str = ""
    escalated_by: str = ""
    reason: str = ""


@dataclass(frozen=True)
class ReviewResolved(DomainEvent):
    """Fired when a review task is approved or rejected."""
    task_id: str = ""
    doc_id: str = ""
    action: str = ""  # "approved" | "rejected"
    resolved_by: str = ""


# =============================================================================
# Report Events
# =============================================================================

@dataclass(frozen=True)
class ReportGenerated(DomainEvent):
    """Fired when an audit report is generated."""
    doc_id: str = ""
    report_path: str = ""


# =============================================================================
# Evidence Graph Events
# =============================================================================

@dataclass(frozen=True)
class EvidenceLinkCreated(DomainEvent):
    """Fired when a new evidence relationship is established."""
    source_id: str = ""
    target_id: str = ""
    relationship_type: str = ""
    confidence: float = 0.0
