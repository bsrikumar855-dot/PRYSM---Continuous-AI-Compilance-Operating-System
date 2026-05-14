"""ComplianceAgent — maps extracted entities to rule engine inputs."""

from app.agents.base import BaseAgent, AgentContext


class ComplianceAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ComplianceAgent"

    async def execute(self, context: AgentContext) -> AgentContext:
        """Translate extracted entities into structured rule inputs."""
        # TODO: Map entities to domain-specific rule inputs
        return context
