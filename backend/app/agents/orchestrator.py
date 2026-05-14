"""Agent orchestrator — sequences agent execution with shared context."""

from app.agents.base import BaseAgent, AgentContext
from app.logging.logger import get_logger

logger = get_logger(__name__)


class AgentOrchestrator:
    """Executes a sequence of agents, passing shared context through the pipeline."""

    def __init__(self):
        self._agents: list[BaseAgent] = []

    def register(self, agent: BaseAgent):
        self._agents.append(agent)
        return self

    async def run(self, context: AgentContext) -> AgentContext:
        """Execute all registered agents in sequence."""
        for agent in self._agents:
            logger.info(f"Running agent: {agent.name}")
            try:
                context = await agent.execute(context)
            except Exception as e:
                logger.error(f"Agent {agent.name} failed: {e}")
                raise
        return context
