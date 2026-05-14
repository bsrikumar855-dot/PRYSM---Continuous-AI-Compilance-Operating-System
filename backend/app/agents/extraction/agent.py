"""ExtractionAgent — extracts structured entities from OCR text via LLM."""

from app.agents.base import BaseAgent, AgentContext


class ExtractionAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "ExtractionAgent"

    async def execute(self, context: AgentContext) -> AgentContext:
        """Extract entities from OCR text using LLM."""
        # TODO: Call AI client with extraction prompts
        # context.extracted_entities = extracted
        return context
