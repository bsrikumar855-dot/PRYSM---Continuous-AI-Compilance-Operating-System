"""AI Copilot chat endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CopilotQuery(BaseModel):
    message: str
    document_id: str | None = None


@router.post("/chat")
async def copilot_chat(query: CopilotQuery):
    """Send a message to the AI compliance copilot."""
    return {"response": "", "sources": []}


@router.get("/suggestions/{document_id}")
async def get_suggestions(document_id: str):
    """Get AI-powered compliance suggestions for a document."""
    return {"document_id": document_id, "suggestions": []}
