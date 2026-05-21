"""Review workflow — assignment and resolution pipeline."""


class ReviewWorkflow:
    async def assign_review(self, document_id: str, compliance_results: list):
        """Create and assign review tasks based on compliance results."""
        pass

    async def resolve(self, task_id: str, action: str, notes: str = None):
        """Resolve a review task."""
        pass
