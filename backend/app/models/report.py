"""Report ORM model."""

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    report_type = Column(String, default="compliance")
    status = Column(String, default="generating")
    file_path = Column(String, nullable=True)
    compliance_score = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    total_rules = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    warnings = Column(Integer, default=0)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
