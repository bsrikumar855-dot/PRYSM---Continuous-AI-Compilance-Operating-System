"""Review repository."""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.review_task import ReviewTask


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> ReviewTask:
        task = ReviewTask(**kwargs)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_queue(self, status: str = "pending") -> List[ReviewTask]:
        return self.db.query(ReviewTask).filter(ReviewTask.status == status).all()

    def get_by_id(self, task_id: str) -> Optional[ReviewTask]:
        return self.db.query(ReviewTask).filter(ReviewTask.id == task_id).first()

    def update_status(self, task_id: str, status: str, notes: str = None):
        task = self.get_by_id(task_id)
        if task:
            task.status = status
            if notes:
                task.notes = notes
            self.db.commit()
        return task
