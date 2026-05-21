"""Compliance check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/results")
async def list_compliance_results():
    """List all compliance check results."""
    return {"results": []}


@router.get("/results/{document_id}")
async def get_compliance_result(document_id: str):
    """Get compliance results for a specific document."""
    return {"document_id": document_id, "results": []}


@router.post("/run/{document_id}")
async def run_compliance_check(document_id: str):
    """Trigger compliance check for a document."""
    return {"message": "Compliance check initiated", "document_id": document_id}
