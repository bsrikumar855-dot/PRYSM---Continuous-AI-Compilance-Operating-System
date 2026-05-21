"""Compliance service — orchestrates rule engine checks."""

from sqlalchemy.orm import Session
from app.repositories.compliance_repo import ComplianceRepository
from app.engine.runner import RuleRunner


class ComplianceService:
    def __init__(self, db: Session):
        self.repo = ComplianceRepository(db)
        self.runner = RuleRunner()

    async def run_check(self, document_id: str, extracted_data: dict):
        """Run compliance rules against extracted document data."""
        results = self.runner.execute(extracted_data)
        # Persist results
        records = self.repo.save_results(
            [{"document_id": document_id, **r} for r in results]
        )
        return records

    async def get_results(self, document_id: str):
        return self.repo.get_by_document(document_id)
