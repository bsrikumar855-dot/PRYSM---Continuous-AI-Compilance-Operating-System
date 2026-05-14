"""Copilot conversation memory."""

from typing import List, Dict


class ConversationMemory:
    """Manages conversation history for copilot sessions."""

    def __init__(self, max_turns: int = 20):
        self._sessions: Dict[str, List[dict]] = {}
        self._max_turns = max_turns

    def add_turn(self, session_id: str, role: str, content: str):
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append({"role": role, "content": content})
        # Trim to max turns
        if len(self._sessions[session_id]) > self._max_turns:
            self._sessions[session_id] = self._sessions[session_id][-self._max_turns:]

    def get_history(self, session_id: str) -> List[dict]:
        return self._sessions.get(session_id, [])

    def clear(self, session_id: str):
        self._sessions.pop(session_id, None)
