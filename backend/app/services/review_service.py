"""Review service."""

from sqlalchemy.orm import Session
from app.repositories.review_repo import ReviewRepository


class ReviewService:
    def __init__(self, db: Session):
        self.repo = ReviewRepository(db)

    async def get_queue(self):
        return self.repo.get_queue()

    async def approve(self, task_id: str, notes: str = None):
        return self.repo.update_status(task_id, "approved", notes)

    async def reject(self, task_id: str, notes: str = None):
        return self.repo.update_status(task_id, "rejected", notes)
