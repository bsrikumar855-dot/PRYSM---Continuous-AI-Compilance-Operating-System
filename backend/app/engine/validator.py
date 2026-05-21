"""Input validator for rule engine."""

from typing import Dict, Any, List


class RuleInputValidator:
    """Validates extracted data before rule execution."""

    @staticmethod
    def validate(data: Dict[str, Any], required_fields: List[str]) -> tuple[bool, List[str]]:
        """Check that required fields exist in the extracted data."""
        missing = [f for f in required_fields if f not in data or data[f] is None]
        return len(missing) == 0, missing
