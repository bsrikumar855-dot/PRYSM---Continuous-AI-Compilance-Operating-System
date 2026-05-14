"""Audit trail logger — records all compliance-relevant actions."""

from app.logging.logger import get_logger

audit_logger = get_logger("audit")


def log_audit_event(action: str, entity_type: str, entity_id: str, actor: str = "system", details: dict = None):
    """Log an audit event for compliance trail."""
    audit_logger.info(
        f"AUDIT | action={action} | entity={entity_type}:{entity_id} | actor={actor} | details={details or {}}"
    )
