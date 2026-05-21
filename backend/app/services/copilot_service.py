"""Copilot service — AI-powered compliance assistant."""


class CopilotService:
    async def chat(self, message: str, document_id: str = None, session_id: str = None):
        """Process copilot chat message."""
        # TODO: Delegate to CopilotAgent
        return {"response": "", "sources": [], "session_id": session_id or ""}

    async def get_suggestions(self, document_id: str):
        """Get AI compliance suggestions for a document."""
        # TODO: Delegate to CopilotAgent
        return []
