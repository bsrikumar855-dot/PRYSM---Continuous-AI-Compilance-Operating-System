"""Document service — business logic for document management."""

from sqlalchemy.orm import Session
from app.repositories.document_repo import DocumentRepository


class DocumentService:
    def __init__(self, db: Session):
        self.repo = DocumentRepository(db)

    async def upload(self, filename: str, file_path: str, file_size: int):
        """Process document upload and initiate ingestion workflow."""
        doc = self.repo.create(
            filename=filename,
            original_filename=filename,
            file_path=file_path,
            file_size_bytes=file_size,
        )
        # TODO: Trigger ingestion workflow
        return doc

    async def get_document(self, document_id: str):
        return self.repo.get_by_id(document_id)

    async def list_documents(self, skip: int = 0, limit: int = 20):
        return self.repo.list_all(skip=skip, limit=limit)

    async def delete_document(self, document_id: str):
        return self.repo.delete(document_id)
