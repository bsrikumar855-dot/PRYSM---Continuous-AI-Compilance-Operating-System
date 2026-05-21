"""Copilot schemas."""

from pydantic import BaseModel
from typing import List, Optional


class CopilotMessage(BaseModel):
    message: str
    document_id: Optional[str] = None
    session_id: Optional[str] = None


class CopilotResponse(BaseModel):
    response: str
    sources: List[dict] = []
    suggestions: List[str] = []
    session_id: str
