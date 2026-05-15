"""
PRYSM Backend — Application Entry Point
==========================================
FastAPI application factory with API v1 versioning,
middleware stack, and consolidated router registration.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.db.init_db import init_db
from app.middleware.request_id import RequestIdMiddleware

# Import routers
from app.routers import (
    analyze,
    dashboard,
    extract,
    health,
    reports,
    risks,
    upload,
)

# Register default event handlers on import
import app.events.handlers  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="PRYSM Backend",
        description="Continuous AI Compliance Operating System",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── Middleware Stack (order matters: outermost first) ─────────────
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception Handlers ────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Health (no prefix) ────────────────────────────────────────────
    app.include_router(health.router, tags=["health"])

    # ── API v1 Routes ─────────────────────────────────────────────────
    app.include_router(upload.router, prefix="/api/v1", tags=["documents"])
    app.include_router(extract.router, prefix="/api/v1", tags=["documents"])
    app.include_router(analyze.router, prefix="/api/v1", tags=["compliance"])
    app.include_router(risks.router, prefix="/api/v1", tags=["risks"])
    app.include_router(dashboard.router, prefix="/api/v1", tags=["dashboard"])
    app.include_router(reports.router, prefix="/api/v1", tags=["reports"])

    return app


app = create_app()
