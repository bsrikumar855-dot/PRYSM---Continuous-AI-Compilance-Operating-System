"""
PRYSM Standardized API Response Schemas
==========================================
Centralized response envelope for consistent API behavior.
All API endpoints should use these patterns.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""
    success: bool = True
    data: T | None = None
    error: ErrorDetail | None = None
    meta: ResponseMeta | None = None


class ErrorDetail(BaseModel):
    """Structured error information."""
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ResponseMeta(BaseModel):
    """Response metadata for pagination and traceability."""
    request_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    page: int | None = None
    page_size: int | None = None
    total_count: int | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""
    success: bool = True
    data: list[T] = Field(default_factory=list)
    meta: ResponseMeta | None = None


# =============================================================================
# Helper factories
# =============================================================================

def success_response(data: Any = None, meta: dict | None = None) -> dict:
    """Build a standard success response dict."""
    response = {"success": True, "data": data}
    if meta:
        response["meta"] = meta
    return response


def error_response(
    code: str, message: str, status_code: int = 400, details: dict | None = None
) -> dict:
    """Build a standard error response dict."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }
