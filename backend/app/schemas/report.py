"""Report schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReportSummary(BaseModel):
    id: str
    document_id: str
    report_type: str
    status: str
    generated_at: datetime
    download_url: Optional[str] = None


class ReportDetail(ReportSummary):
    compliance_score: float
    total_rules_checked: int
    passed: int
    failed: int
    warnings: int
    risk_score: float
