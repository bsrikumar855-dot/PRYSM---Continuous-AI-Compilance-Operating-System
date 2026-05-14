"""ROC Rules v1 — CIN validation, filing compliance."""

import re
from typing import Dict, Any
from app.engine.rules.base import BaseRule
from app.engine.registry import register_rule


@register_rule("roc")
class CINFormatRule(BaseRule):
    @property
    def rule_id(self) -> str:
        return "ROC-001"

    @property
    def name(self) -> str:
        return "CIN Format Validation"

    @property
    def domain(self) -> str:
        return "roc"

    @property
    def severity(self) -> str:
        return "critical"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        cin = data.get("cin", "")
        if not cin:
            return self._result("warning", "CIN not found in document")

        # CIN: 21-char alphanumeric
        if len(cin) == 21 and re.match(r"^[A-Z0-9]+$", cin):
            return self._result("pass", f"CIN {cin} format is valid")
        return self._result("fail", f"CIN {cin} has invalid format")
