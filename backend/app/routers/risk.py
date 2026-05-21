"""Risk intelligence endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
async def risk_overview():
    """Get overall risk dashboard data."""
    return {"risk_summary": {}}


@router.get("/flags/{document_id}")
async def get_risk_flags(document_id: str):
    """Get risk flags for a specific document."""
    return {"document_id": document_id, "flags": []}
