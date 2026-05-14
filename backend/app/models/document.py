"""Document ORM model."""

from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    document_type = Column(String, nullable=True)
    status = Column(String, default="uploaded")
    file_path = Column(String, nullable=False)
    file_size_bytes = Column(Integer, default=0)
    page_count = Column(Integer, default=0)
    mime_type = Column(String, nullable=True)
    ocr_text = Column(Text, nullable=True)
    extracted_entities = Column(JSON, default=dict)
    metadata_ = Column("metadata", JSON, default=dict)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
