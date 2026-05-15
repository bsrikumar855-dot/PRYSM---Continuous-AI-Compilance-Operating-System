"""
PRYSM Default Event Handlers
===============================
Built-in handlers for audit logging and traceability.
Additional handlers can be registered in service modules.
"""

import logging

from app.events.bus import event_bus
from app.events.types import (
    AnalysisCompleted,
    DocumentStatusChanged,
    DocumentUploaded,
    ExtractionCompleted,
    ExtractionFailed,
    ReportGenerated,
    ReviewEscalated,
    ReviewResolved,
    RiskDetected,
)

logger = logging.getLogger("prysm.events")


# =============================================================================
# Audit Trail Handlers — log every significant event for compliance
# =============================================================================

@event_bus.on(DocumentUploaded)
def _log_document_uploaded(event: DocumentUploaded) -> None:
    logger.info(
        "audit.document_uploaded",
        extra={"doc_id": event.doc_id, "filename": event.filename},
    )


@event_bus.on(DocumentStatusChanged)
def _log_status_changed(event: DocumentStatusChanged) -> None:
    logger.info(
        "audit.status_changed",
        extra={
            "doc_id": event.doc_id,
            "from": event.from_status,
            "to": event.to_status,
        },
    )


@event_bus.on(ExtractionCompleted)
def _log_extraction_completed(event: ExtractionCompleted) -> None:
    logger.info(
        "audit.extraction_completed",
        extra={
            "doc_id": event.doc_id,
            "confidence": event.confidence,
        },
    )


@event_bus.on(ExtractionFailed)
def _log_extraction_failed(event: ExtractionFailed) -> None:
    logger.warning(
        "audit.extraction_failed",
        extra={"doc_id": event.doc_id, "error": event.error},
    )


@event_bus.on(AnalysisCompleted)
def _log_analysis_completed(event: AnalysisCompleted) -> None:
    logger.info(
        "audit.analysis_completed",
        extra={
            "doc_id": event.doc_id,
            "findings": event.finding_count,
            "critical": event.critical_count,
        },
    )


@event_bus.on(RiskDetected)
def _log_risk_detected(event: RiskDetected) -> None:
    logger.warning(
        "audit.risk_detected",
        extra={
            "doc_id": event.doc_id,
            "rule_id": event.rule_id,
            "severity": event.severity,
        },
    )


@event_bus.on(ReviewEscalated)
def _log_review_escalated(event: ReviewEscalated) -> None:
    logger.warning(
        "audit.review_escalated",
        extra={"task_id": event.task_id, "doc_id": event.doc_id},
    )


@event_bus.on(ReviewResolved)
def _log_review_resolved(event: ReviewResolved) -> None:
    logger.info(
        "audit.review_resolved",
        extra={
            "task_id": event.task_id,
            "doc_id": event.doc_id,
            "action": event.action,
        },
    )


@event_bus.on(ReportGenerated)
def _log_report_generated(event: ReportGenerated) -> None:
    logger.info(
        "audit.report_generated",
        extra={"doc_id": event.doc_id, "path": event.report_path},
    )
