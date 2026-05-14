"""Common shared schemas."""

from pydantic import BaseModel
from typing import Optional


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


class StatusResponse(BaseModel):
    success: bool
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
