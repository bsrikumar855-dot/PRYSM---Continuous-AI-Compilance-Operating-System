"""Invoice Rules v1 — mandatory field checks, amount validation."""

from typing import Dict, Any
from app.engine.rules.base import BaseRule
from app.engine.registry import register_rule


@register_rule("invoice")
class InvoiceMandatoryFieldsRule(BaseRule):
    REQUIRED = ["invoice_number", "invoice_date", "total_amount", "vendor_name"]

    @property
    def rule_id(self) -> str:
        return "INV-001"

    @property
    def name(self) -> str:
        return "Invoice Mandatory Fields"

    @property
    def domain(self) -> str:
        return "invoice"

    @property
    def severity(self) -> str:
        return "critical"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        missing = [f for f in self.REQUIRED if not data.get(f)]
        if not missing:
            return self._result("pass", "All mandatory invoice fields present")
        return self._result("fail", f"Missing mandatory fields: {', '.join(missing)}")


@register_rule("invoice")
class InvoiceAmountConsistencyRule(BaseRule):
    @property
    def rule_id(self) -> str:
        return "INV-002"

    @property
    def name(self) -> str:
        return "Invoice Amount Consistency"

    @property
    def domain(self) -> str:
        return "invoice"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        subtotal = data.get("subtotal", 0)
        tax = data.get("tax_amount", 0)
        total = data.get("total_amount", 0)

        if not all([subtotal, total]):
            return self._result("warning", "Cannot verify — subtotal or total missing")

        expected = round(subtotal + tax, 2)
        if abs(expected - total) < 0.01:
            return self._result("pass", f"Amount consistent: {subtotal} + {tax} = {total}")
        return self._result("fail", f"Amount mismatch: {subtotal} + {tax} = {expected}, but total is {total}")
