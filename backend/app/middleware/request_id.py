"""
PRYSM Request Middleware
==========================
Request ID injection and request/response logging.
"""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logging import generate_request_id, get_logger, request_id_ctx

logger = get_logger("middleware")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Inject a unique request ID into every request for traceability."""

    async def dispatch(self, request: Request, call_next) -> Response:
        rid = request.headers.get("X-Request-ID") or generate_request_id()
        request_id_ctx.set(rid)
        start = time.time()
        response = await call_next(request)
        duration = round(time.time() - start, 3)
        response.headers["X-Request-ID"] = rid
        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_s": duration,
                "request_id": rid,
            },
        )
        return response
