"""CopilotAgent — interactive Q&A over compliance data."""

from app.agents.base import BaseAgent, AgentContext


class CopilotAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "CopilotAgent"

    async def execute(self, context: AgentContext) -> AgentContext:
        """Answer user questions about compliance findings."""
        # TODO: RAG-based Q&A using vector store + compliance context
        return context
