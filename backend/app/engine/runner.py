"""Rule execution engine — runs deterministic compliance rules."""

from typing import List, Dict, Any
from app.engine.registry import RuleRegistry
from app.logging.logger import get_logger

logger = get_logger(__name__)


class RuleRunner:
    """Executes registered compliance rules against extracted data."""

    def __init__(self):
        self.registry = RuleRegistry()

    def execute(self, extracted_data: Dict[str, Any], domains: List[str] = None) -> List[dict]:
        """Run all applicable rules and return results."""
        results = []
        rules = self.registry.get_rules(domains=domains)

        for rule in rules:
            try:
                result = rule.evaluate(extracted_data)
                results.append(result)
            except Exception as e:
                logger.error(f"Rule {rule.rule_id} failed: {e}")
                results.append({
                    "rule_id": rule.rule_id,
                    "rule_name": rule.name,
                    "domain": rule.domain,
                    "status": "error",
                    "severity": "high",
                    "message": f"Rule execution error: {str(e)}",
                })

        return results
