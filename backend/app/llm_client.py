"""Minimal Groq chat-completions client for the PRYSM copilot."""

import httpx


GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"


class LLMServiceError(RuntimeError):
    """Raised when the configured language model cannot return an answer."""


def create_chat_completion(
    messages: list[dict[str, str]],
    api_key: str,
    primary_model: str,
    fallback_model: str | None = None,
) -> tuple[str, str]:
    """Create a chat completion and retry with a fallback model if configured."""
    if not api_key:
        raise LLMServiceError("GROQ_API_KEY is not configured")

    models = [primary_model]
    if fallback_model and fallback_model != primary_model:
        models.append(fallback_model)

    last_error = "No model responded"
    for model in models:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.35,
            "max_completion_tokens": 1400,
        }
        try:
            response = httpx.post(
                GROQ_CHAT_COMPLETIONS_URL,
                json=payload,
                timeout=35,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            body = response.json()
            content = body["choices"][0]["message"]["content"].strip()
            if content:
                return content, model
            last_error = f"{model} returned an empty response"
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            last_error = f"{model} failed: {exc}"

    raise LLMServiceError(last_error)
