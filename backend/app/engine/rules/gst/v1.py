"""GST Rules v1 — GSTIN format validation, rate checks."""

import re
from typing import Dict, Any
from app.engine.rules.base import BaseRule
from app.engine.registry import register_rule


@register_rule("gst")
class GSTINFormatRule(BaseRule):
    """Validates GSTIN format (15-char alphanumeric)."""

    @property
    def rule_id(self) -> str:
        return "GST-001"

    @property
    def name(self) -> str:
        return "GSTIN Format Validation"

    @property
    def domain(self) -> str:
        return "gst"

    @property
    def severity(self) -> str:
        return "critical"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        gstin = data.get("gstin", "")
        if not gstin:
            return self._result("warning", "GSTIN not found in document")

        pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
        if re.match(pattern, gstin):
            return self._result("pass", f"GSTIN {gstin} format is valid")
        return self._result("fail", f"GSTIN {gstin} has invalid format")


@register_rule("gst")
class GSTRateRule(BaseRule):
    """Validates GST rate is within allowed slabs."""

    VALID_RATES = [0, 5, 12, 18, 28]

    @property
    def rule_id(self) -> str:
        return "GST-002"

    @property
    def name(self) -> str:
        return "GST Rate Slab Validation"

    @property
    def domain(self) -> str:
        return "gst"

    @property
    def severity(self) -> str:
        return "high"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        rate = data.get("gst_rate")
        if rate is None:
            return self._result("warning", "GST rate not found in document")

        if rate in self.VALID_RATES:
            return self._result("pass", f"GST rate {rate}% is valid")
        return self._result("fail", f"GST rate {rate}% is not a valid slab ({self.VALID_RATES})")
