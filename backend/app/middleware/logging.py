"""Request/response logging middleware."""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.logger import get_logger

logger = get_logger("middleware.logging")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round(time.time() - start, 3)
        logger.info(
            f"{request.method} {request.url.path} → {response.status_code} ({duration}s)"
        )
        return response
