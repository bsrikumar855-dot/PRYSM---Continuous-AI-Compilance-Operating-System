"""Document repository — database operations for documents."""

from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Document:
        doc = Document(**kwargs)
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def get_by_id(self, document_id: str) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def list_all(self, skip: int = 0, limit: int = 20) -> List[Document]:
        return self.db.query(Document).offset(skip).limit(limit).all()

    def update_status(self, document_id: str, status: str) -> Optional[Document]:
        doc = self.get_by_id(document_id)
        if doc:
            doc.status = status
            self.db.commit()
            self.db.refresh(doc)
        return doc

    def delete(self, document_id: str) -> bool:
        doc = self.get_by_id(document_id)
        if doc:
            self.db.delete(doc)
            self.db.commit()
            return True
        return False
