"""Response parsers for extraction agent."""


def parse_extraction_response(raw_response: str) -> dict:
    """Parse LLM response into structured entity dict."""
    import json
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {"raw": raw_response, "parse_error": True}
