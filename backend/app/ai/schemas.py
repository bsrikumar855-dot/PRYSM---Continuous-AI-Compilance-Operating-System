"""AI response schemas for structured output."""

from pydantic import BaseModel
from typing import List, Optional


class ExtractedEntity(BaseModel):
    field: str
    value: str
    confidence: float
    source_page: Optional[int] = None


class ExtractionResult(BaseModel):
    entities: List[ExtractedEntity]
    document_type: str
    raw_text_length: int
