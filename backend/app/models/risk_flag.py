"""Risk flag ORM model."""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class RiskFlag(Base):
    __tablename__ = "risk_flags"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    risk_level = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    recommendation = Column(String, nullable=True)
    score = Column(Float, default=0.0)
    evidence_ref = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
