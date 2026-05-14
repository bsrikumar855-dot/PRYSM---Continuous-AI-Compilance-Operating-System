"""TDS Rules v1 — TAN validation, rate checks."""

import re
from typing import Dict, Any
from app.engine.rules.base import BaseRule
from app.engine.registry import register_rule


@register_rule("tds")
class TANFormatRule(BaseRule):
    @property
    def rule_id(self) -> str:
        return "TDS-001"

    @property
    def name(self) -> str:
        return "TAN Format Validation"

    @property
    def domain(self) -> str:
        return "tds"

    @property
    def severity(self) -> str:
        return "critical"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        tan = data.get("tan", "")
        if not tan:
            return self._result("warning", "TAN not found in document")

        # TAN: 10-char (4 alpha + 5 digits + 1 alpha)
        if re.match(r"^[A-Z]{4}[0-9]{5}[A-Z]$", tan):
            return self._result("pass", f"TAN {tan} format is valid")
        return self._result("fail", f"TAN {tan} has invalid format")
