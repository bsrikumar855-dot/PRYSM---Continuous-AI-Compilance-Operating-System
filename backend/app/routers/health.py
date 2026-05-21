"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Application health check."""
    return {"status": "healthy", "service": "prysm-api"}
