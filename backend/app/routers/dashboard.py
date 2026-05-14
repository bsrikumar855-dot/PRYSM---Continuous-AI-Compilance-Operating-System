"""Dashboard data endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def dashboard_summary():
    """Get dashboard summary metrics."""
    return {
        "total_documents": 0,
        "compliance_score": 0.0,
        "pending_reviews": 0,
        "critical_risks": 0,
        "recent_activity": [],
    }


@router.get("/compliance-trend")
async def compliance_trend():
    """Get compliance score trend over time."""
    return {"trend": []}
