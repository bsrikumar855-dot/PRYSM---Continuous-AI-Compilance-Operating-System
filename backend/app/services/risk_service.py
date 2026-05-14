"""Risk service."""

from sqlalchemy.orm import Session
from app.repositories.risk_repo import RiskRepository


class RiskService:
    def __init__(self, db: Session):
        self.repo = RiskRepository(db)

    async def get_flags(self, document_id: str):
        return self.repo.get_by_document(document_id)
