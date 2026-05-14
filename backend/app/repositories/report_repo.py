"""Report repository."""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.report import Report


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Report:
        report = Report(**kwargs)
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_by_id(self, report_id: str) -> Optional[Report]:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def list_all(self) -> List[Report]:
        return self.db.query(Report).all()
