"""Audit log ORM model."""

from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    actor = Column(String, nullable=True)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
