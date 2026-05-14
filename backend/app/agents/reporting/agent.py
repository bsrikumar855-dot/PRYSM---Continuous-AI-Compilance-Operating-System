"""ReportingAgent — generates narrative summaries for audit reports."""

from app.agents.base import BaseAgent, AgentContext


class ReportingAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ReportingAgent"

    async def execute(self, context: AgentContext) -> AgentContext:
        """Generate human-readable narrative for compliance reports."""
        # TODO: Create executive summary, findings narrative, recommendations
        return context
