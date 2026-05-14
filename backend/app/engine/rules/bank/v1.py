"""Bank Rules v1 — balance reconciliation, duplicate detection."""

from typing import Dict, Any
from app.engine.rules.base import BaseRule
from app.engine.registry import register_rule


@register_rule("bank")
class BankBalanceReconciliationRule(BaseRule):
    @property
    def rule_id(self) -> str:
        return "BANK-001"

    @property
    def name(self) -> str:
        return "Bank Balance Reconciliation"

    @property
    def domain(self) -> str:
        return "bank"

    @property
    def severity(self) -> str:
        return "high"

    def evaluate(self, data: Dict[str, Any]) -> dict:
        opening = data.get("opening_balance", 0)
        closing = data.get("closing_balance", 0)
        total_credits = data.get("total_credits", 0)
        total_debits = data.get("total_debits", 0)

        if not any([opening, closing]):
            return self._result("warning", "Balance data not available")

        expected_closing = opening + total_credits - total_debits
        if abs(expected_closing - closing) < 0.01:
            return self._result("pass", "Bank balance reconciles correctly")
        return self._result("fail", f"Balance mismatch: expected {expected_closing}, found {closing}")
