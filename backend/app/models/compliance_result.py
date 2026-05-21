"""Compliance result ORM model."""

from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    rule_id = Column(String, nullable=False)
    rule_name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    status = Column(String, nullable=False)  # pass | fail | warning
    severity = Column(String, nullable=False)
    message = Column(String, nullable=True)
    evidence_ref = Column(String, nullable=True)
    details = Column(JSON, default=dict)
    overall_score = Column(Float, nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
