"""
PRYSM Enterprise Error Handling
==================================
Centralized exception hierarchy and API error response handlers.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.logging import request_id_ctx

logger = logging.getLogger(__name__)


# =============================================================================
# Exception Hierarchy
# =============================================================================

class PRYSMError(Exception):
    """Base exception for all PRYSM application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        code: str = "INTERNAL_ERROR",
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        super().__init__(message)


class DocumentNotFoundError(PRYSMError):
    def __init__(self, doc_id: str):
        super().__init__(
            "Document not found",
            status_code=404,
            code="DOCUMENT_NOT_FOUND",
            details={"doc_id": doc_id},
        )


class InvalidFileTypeError(PRYSMError):
    def __init__(self, content_type: str):
        super().__init__(
            "Invalid file type",
            status_code=400,
            code="INVALID_FILE_TYPE",
            details={"content_type": content_type},
        )


class ExtractionError(PRYSMError):
    def __init__(self, message: str = "Extraction failed", **kwargs: Any):
        super().__init__(message, status_code=500, code="EXTRACTION_ERROR", **kwargs)


class AnalysisError(PRYSMError):
    def __init__(self, message: str = "Analysis failed", **kwargs: Any):
        super().__init__(message, code="ANALYSIS_ERROR", **kwargs)


class ReportGenerationError(PRYSMError):
    def __init__(self, message: str = "Report generation failed", **kwargs: Any):
        super().__init__(message, status_code=500, code="REPORT_ERROR", **kwargs)


class InvalidTransitionError(PRYSMError):
    def __init__(self, entity_type: str, entity_id: str, current: str, target: str):
        super().__init__(
            f"Invalid {entity_type} transition: {current} → {target}",
            status_code=409,
            code="INVALID_STATE_TRANSITION",
            details={
                "entity_type": entity_type,
                "entity_id": entity_id,
                "current_state": current,
                "target_state": target,
            },
        )


class ValidationError(PRYSMError):
    def __init__(self, message: str, field: str = "", **kwargs: Any):
        super().__init__(
            message,
            status_code=422,
            code="VALIDATION_ERROR",
            details={"field": field, **kwargs.get("details", {})},
        )


# =============================================================================
# Error Response Builder
# =============================================================================

def _build_error_response(
    status_code: int, code: str, message: str, details: dict | None = None
) -> JSONResponse:
    """Build a consistent error JSON response."""
    body: dict[str, Any] = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details:
        body["error"]["details"] = details
    rid = request_id_ctx.get("")
    if rid:
        body["meta"] = {"request_id": rid}
    return JSONResponse(status_code=status_code, content=body)


# =============================================================================
# Exception Handler Registration
# =============================================================================

def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""

    @app.exception_handler(PRYSMError)
    async def handle_prysm_error(_: Request, exc: PRYSMError) -> JSONResponse:
        logger.warning(
            "prysm_error",
            extra={"code": exc.code, "message": exc.message, "details": exc.details},
        )
        return _build_error_response(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(HTTPException)
    async def handle_http_error(_: Request, exc: HTTPException) -> JSONResponse:
        return _build_error_response(exc.status_code, "HTTP_ERROR", str(exc.detail))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled_error")
        return _build_error_response(500, "INTERNAL_ERROR", "Internal server error")
