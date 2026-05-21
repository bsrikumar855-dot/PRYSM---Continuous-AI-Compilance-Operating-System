"""Risk schemas."""

from pydantic import BaseModel
from typing import List, Optional


class RiskFlag(BaseModel):
    id: str
    document_id: str
    risk_level: str  # critical | high | medium | low | info
    category: str
    description: str
    recommendation: str
    evidence_ref: Optional[str] = None


class RiskOverview(BaseModel):
    total_flags: int
    critical: int
    high: int
    medium: int
    low: int
    risk_score: float
    flags: List[RiskFlag]
