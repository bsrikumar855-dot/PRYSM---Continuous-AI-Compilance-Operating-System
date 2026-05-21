"""Audit log repository."""

from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log(self, action: str, entity_type: str, entity_id: str, actor: str = None, details: dict = None):
        entry = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            details=details or {},
        )
        self.db.add(entry)
        self.db.commit()
        return entry
