"""Risk repository."""

from sqlalchemy.orm import Session
from typing import List
from app.models.risk_flag import RiskFlag


class RiskRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_flags(self, flags: List[dict]) -> List[RiskFlag]:
        records = [RiskFlag(**f) for f in flags]
        self.db.add_all(records)
        self.db.commit()
        return records

    def get_by_document(self, document_id: str) -> List[RiskFlag]:
        return self.db.query(RiskFlag).filter(RiskFlag.document_id == document_id).all()
