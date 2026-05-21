"""Base agent — abstract interface for all PRYSM agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AgentContext:
    """Shared context passed between agents in a pipeline."""
    document_id: str = ""
    ocr_text: str = ""
    extracted_entities: Dict[str, Any] = field(default_factory=dict)
    compliance_results: list = field(default_factory=list)
    risk_flags: list = field(default_factory=list)
    evidence_map: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all PRYSM agents."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent identifier."""
        ...

    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentContext:
        """Execute agent logic and return updated context."""
        ...
