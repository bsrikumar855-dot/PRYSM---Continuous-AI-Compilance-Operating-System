"""Rule registry — discovers and loads compliance rules."""

from typing import List, Optional, Dict, Type
from app.engine.rules.base import BaseRule

# Global rule store
_RULE_REGISTRY: Dict[str, List[Type[BaseRule]]] = {}


def register_rule(domain: str):
    """Decorator to register a rule class in the registry."""
    def decorator(cls):
        if domain not in _RULE_REGISTRY:
            _RULE_REGISTRY[domain] = []
        _RULE_REGISTRY[domain].append(cls)
        return cls
    return decorator


class RuleRegistry:
    """Manages rule discovery and instantiation."""

    def get_rules(self, domains: Optional[List[str]] = None) -> List[BaseRule]:
        """Get all rule instances, optionally filtered by domain."""
        rules = []
        target_domains = domains or list(_RULE_REGISTRY.keys())
        for domain in target_domains:
            for rule_cls in _RULE_REGISTRY.get(domain, []):
                rules.append(rule_cls())
        return rules

    def get_domains(self) -> List[str]:
        return list(_RULE_REGISTRY.keys())
