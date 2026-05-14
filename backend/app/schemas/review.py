"""Review workflow schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewTask(BaseModel):
    id: str
    document_id: str
    assigned_to: Optional[str] = None
    status: str  # pending | in_progress | approved | rejected | escalated
    priority: str
    notes: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None


class ReviewAction(BaseModel):
    action: str  # approve | reject | escalate
    notes: Optional[str] = None
