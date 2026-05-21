"""Authentication middleware."""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Implement JWT/API key validation
        # Skip auth for health check and docs
        if request.url.path in ["/api/health", "/api/docs", "/api/redoc", "/openapi.json"]:
            return await call_next(request)
        return await call_next(request)
