"""Human review workflow endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/queue")
async def get_review_queue():
    """Get pending review tasks."""
    return {"queue": []}


@router.get("/tasks/{task_id}")
async def get_review_task(task_id: str):
    """Get a specific review task."""
    return {"task_id": task_id}


@router.post("/tasks/{task_id}/approve")
async def approve_review(task_id: str):
    """Approve a review task."""
    return {"task_id": task_id, "status": "approved"}


@router.post("/tasks/{task_id}/reject")
async def reject_review(task_id: str):
    """Reject a review task."""
    return {"task_id": task_id, "status": "rejected"}
