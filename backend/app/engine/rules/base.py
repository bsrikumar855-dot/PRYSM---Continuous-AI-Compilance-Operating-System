"""Base rule — abstract interface for all compliance rules."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseRule(ABC):
    """Abstract base for all deterministic compliance rules.

    Rules are pure Python — NO AI calls, NO network calls.
    Each rule returns: pass/fail, severity, evidence_ref, message.
    """

    @property
    @abstractmethod
    def rule_id(self) -> str:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def domain(self) -> str:
        ...

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def severity(self) -> str:
        return "medium"

    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> dict:
        """Evaluate the rule against extracted data.

        Returns:
            dict with keys: rule_id, rule_name, domain, status, severity, message, evidence_ref
        """
        ...

    def _result(self, status: str, message: str, evidence_ref: str = None) -> dict:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.name,
            "domain": self.domain,
            "status": status,
            "severity": self.severity,
            "message": message,
            "evidence_ref": evidence_ref,
        }
