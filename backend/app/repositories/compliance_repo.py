"""Compliance repository."""

from sqlalchemy.orm import Session
from typing import List
from app.models.compliance_result import ComplianceResult


class ComplianceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_results(self, results: List[dict]) -> List[ComplianceResult]:
        records = [ComplianceResult(**r) for r in results]
        self.db.add_all(records)
        self.db.commit()
        return records

    def get_by_document(self, document_id: str) -> List[ComplianceResult]:
        return self.db.query(ComplianceResult).filter(
            ComplianceResult.document_id == document_id
        ).all()
