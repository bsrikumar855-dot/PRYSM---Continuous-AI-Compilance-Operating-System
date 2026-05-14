"""
PRYSM Backend — FastAPI Application Entrypoint
Continuous AI Compliance Operating System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers import (
    health,
    documents,
    compliance,
    risk,
    review,
    reports,
    copilot,
    dashboard,
)
from app.middleware.error_handler import register_error_handlers
from app.middleware.logging import LoggingMiddleware
from app.logging.logger import setup_logging


def create_app() -> FastAPI:
    """Application factory — creates and configures the FastAPI app."""

    setup_logging()

    app = FastAPI(
        title="PRYSM API",
        description="Continuous AI Compliance Operating System",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # --- Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)

    # --- Error Handlers ---
    register_error_handlers(app)

    # --- Routers ---
    api_prefix = "/api/v1"
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(documents.router, prefix=f"{api_prefix}/documents", tags=["Documents"])
    app.include_router(compliance.router, prefix=f"{api_prefix}/compliance", tags=["Compliance"])
    app.include_router(risk.router, prefix=f"{api_prefix}/risk", tags=["Risk"])
    app.include_router(review.router, prefix=f"{api_prefix}/review", tags=["Review"])
    app.include_router(reports.router, prefix=f"{api_prefix}/reports", tags=["Reports"])
    app.include_router(copilot.router, prefix=f"{api_prefix}/copilot", tags=["Copilot"])
    app.include_router(dashboard.router, prefix=f"{api_prefix}/dashboard", tags=["Dashboard"])

    return app


app = create_app()
