"""Compliance schemas."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ComplianceRuleResult(BaseModel):
    rule_id: str
    rule_name: str
    domain: str
    status: str  # pass | fail | warning
    severity: str  # critical | high | medium | low
    message: str
    evidence_ref: Optional[str] = None


class ComplianceCheckResponse(BaseModel):
    document_id: str
    overall_status: str
    score: float
    results: List[ComplianceRuleResult]
    checked_at: datetime
