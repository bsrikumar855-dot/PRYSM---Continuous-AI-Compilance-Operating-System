"""Document schemas — request/response models."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    document_type: Optional[str] = None
    status: str = "uploaded"
    uploaded_at: datetime


class DocumentDetail(BaseModel):
    id: str
    filename: str
    document_type: Optional[str] = None
    status: str
    page_count: int = 0
    file_size_bytes: int = 0
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    extracted_entities: dict = {}


class DocumentListResponse(BaseModel):
    documents: List[DocumentDetail]
    total: int
    page: int = 1
    page_size: int = 20
