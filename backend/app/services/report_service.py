"""Report service."""

from sqlalchemy.orm import Session
from app.repositories.report_repo import ReportRepository


class ReportService:
    def __init__(self, db: Session):
        self.repo = ReportRepository(db)

    async def generate(self, document_id: str):
        """Generate compliance report for a document."""
        report = self.repo.create(document_id=document_id)
        # TODO: Delegate to ReportingAgent + PDF generator
        return report

    async def get_report(self, report_id: str):
        return self.repo.get_by_id(report_id)

    async def list_reports(self):
        return self.repo.list_all()
