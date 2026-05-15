"""
PRYSM Processing State Machine
================================
Centralized state transition logic for document lifecycle and finding workflows.
Enforces valid transitions and provides audit-safe state changes.

Usage:
    from app.core.state_machine import DocumentStateMachine, FindingStateMachine

    machine = DocumentStateMachine()
    machine.transition(document, DocumentStatus.EXTRACTING)  # validates + updates
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from app.core.enums import DocumentStatus, FindingStatus

logger = logging.getLogger(__name__)


# =============================================================================
# Transition Maps
# =============================================================================

DOCUMENT_TRANSITIONS: dict[DocumentStatus, set[DocumentStatus]] = {
    DocumentStatus.UPLOADED: {
        DocumentStatus.OCR_PROCESSING,
        DocumentStatus.EXTRACTING,
        DocumentStatus.FAILED,
    },
    DocumentStatus.OCR_PROCESSING: {
        DocumentStatus.OCR_COMPLETE,
        DocumentStatus.FAILED,
    },
    DocumentStatus.OCR_COMPLETE: {
        DocumentStatus.EXTRACTING,
        DocumentStatus.FAILED,
    },
    DocumentStatus.EXTRACTING: {
        DocumentStatus.EXTRACTED,
        DocumentStatus.FAILED,
    },
    DocumentStatus.EXTRACTED: {
        DocumentStatus.VALIDATING,
        DocumentStatus.ANALYZING,
        DocumentStatus.FAILED,
    },
    DocumentStatus.VALIDATING: {
        DocumentStatus.ANALYZING,
        DocumentStatus.FAILED,
    },
    DocumentStatus.ANALYZING: {
        DocumentStatus.REVIEW_PENDING,
        DocumentStatus.REPORT_READY,
        DocumentStatus.FAILED,
    },
    DocumentStatus.REVIEW_PENDING: {
        DocumentStatus.REPORT_READY,
        DocumentStatus.ANALYZING,
        DocumentStatus.FAILED,
    },
    DocumentStatus.REPORT_READY: {
        DocumentStatus.COMPLETE,
    },
    DocumentStatus.COMPLETE: set(),
    DocumentStatus.FAILED: {
        DocumentStatus.UPLOADED,  # allow retry from failed
    },
}


FINDING_TRANSITIONS: dict[FindingStatus, set[FindingStatus]] = {
    FindingStatus.OPEN: {
        FindingStatus.UNDER_REVIEW,
        FindingStatus.ESCALATED,
        FindingStatus.RESOLVED,
        FindingStatus.ACCEPTED_RISK,
    },
    FindingStatus.UNDER_REVIEW: {
        FindingStatus.AWAITING_EVIDENCE,
        FindingStatus.ESCALATED,
        FindingStatus.RESOLVED,
        FindingStatus.ACCEPTED_RISK,
    },
    FindingStatus.AWAITING_EVIDENCE: {
        FindingStatus.UNDER_REVIEW,
        FindingStatus.ESCALATED,
        FindingStatus.RESOLVED,
    },
    FindingStatus.ESCALATED: {
        FindingStatus.UNDER_REVIEW,
        FindingStatus.RESOLVED,
        FindingStatus.ACCEPTED_RISK,
    },
    FindingStatus.RESOLVED: set(),
    FindingStatus.ACCEPTED_RISK: set(),
}


# =============================================================================
# Exceptions
# =============================================================================

class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    def __init__(self, entity_type: str, entity_id: str, current: str, target: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.current_state = current
        self.target_state = target
        super().__init__(
            f"Invalid {entity_type} transition: {current} → {target} "
            f"(entity_id={entity_id})"
        )


# =============================================================================
# State Machines
# =============================================================================

class DocumentStateMachine:
    """Validates and executes document status transitions."""

    def can_transition(self, current: DocumentStatus, target: DocumentStatus) -> bool:
        """Check whether a transition is valid without executing it."""
        allowed = DOCUMENT_TRANSITIONS.get(current, set())
        return target in allowed

    def validate_transition(
        self, current: DocumentStatus, target: DocumentStatus, doc_id: str = ""
    ) -> None:
        """Raise InvalidTransitionError if the transition is not allowed."""
        if not self.can_transition(current, target):
            raise InvalidTransitionError("document", doc_id, current, target)

    def transition(self, document: Any, target: DocumentStatus) -> str:
        """Validate and apply a status transition to a document ORM object.

        Args:
            document: ORM Document instance with `.status` and `.doc_id` attrs.
            target: The desired new status.

        Returns:
            The previous status string.
        """
        current = DocumentStatus(document.status)
        self.validate_transition(current, target, getattr(document, "doc_id", ""))
        previous = document.status
        document.status = target.value
        logger.info(
            "document_status_transition",
            extra={
                "doc_id": getattr(document, "doc_id", ""),
                "event": "status_transition",
                "from_status": previous,
                "to_status": target.value,
            },
        )
        return previous

    def get_allowed_transitions(self, current: DocumentStatus) -> list[str]:
        """Return list of valid next states from the current state."""
        return sorted(DOCUMENT_TRANSITIONS.get(current, set()))


class FindingStateMachine:
    """Validates and executes finding status transitions."""

    def can_transition(self, current: FindingStatus, target: FindingStatus) -> bool:
        allowed = FINDING_TRANSITIONS.get(current, set())
        return target in allowed

    def validate_transition(
        self, current: FindingStatus, target: FindingStatus, finding_id: str = ""
    ) -> None:
        if not self.can_transition(current, target):
            raise InvalidTransitionError("finding", finding_id, current, target)

    def transition(self, finding: Any, target: FindingStatus) -> str:
        current = FindingStatus(finding.status)
        self.validate_transition(current, target, getattr(finding, "id", ""))
        previous = finding.status
        finding.status = target.value
        if hasattr(finding, "resolved_at") and target in (
            FindingStatus.RESOLVED,
            FindingStatus.ACCEPTED_RISK,
        ):
            finding.resolved_at = datetime.now(timezone.utc)
        logger.info(
            "finding_status_transition",
            extra={
                "finding_id": getattr(finding, "id", ""),
                "event": "status_transition",
                "from_status": previous,
                "to_status": target.value,
            },
        )
        return previous

    def get_allowed_transitions(self, current: FindingStatus) -> list[str]:
        return sorted(FINDING_TRANSITIONS.get(current, set()))


# =============================================================================
# Module-level singletons for convenience
# =============================================================================

document_state_machine = DocumentStateMachine()
finding_state_machine = FindingStateMachine()
