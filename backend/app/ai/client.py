"""AI client — Groq/LLM provider wrapper."""

from app.config.settings import settings


class AIClient:
    """Abstraction over LLM providers (Groq + LLaMA 3.3)."""

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate LLM response."""
        # TODO: Implement Groq API call
        return ""

    async def generate_json(self, prompt: str, system_prompt: str = None) -> dict:
        """Generate structured JSON response."""
        response = await self.generate(prompt, system_prompt)
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw": response, "parse_error": True}
