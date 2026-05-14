"""EvidenceAgent — maps findings to source document evidence."""

from app.agents.base import BaseAgent, AgentContext


class EvidenceAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "EvidenceAgent"

    async def execute(self, context: AgentContext) -> AgentContext:
        """Map compliance and risk findings back to source document locations."""
        # TODO: Link each finding to specific text/page in source document
        return context
