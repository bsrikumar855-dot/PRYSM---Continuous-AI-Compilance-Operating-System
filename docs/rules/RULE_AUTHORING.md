# Rule Authoring Guide

## Creating a New Rule

1. Create a new file in `backend/app/engine/rules/{domain}/v{version}.py`
2. Extend `BaseRule` and implement `evaluate()`
3. Decorate with `@register_rule("{domain}")`
4. Rules must be **pure Python** — no AI, no network calls

## Example
```python
@register_rule("gst")
class MyRule(BaseRule):
    @property
    def rule_id(self): return "GST-003"

    @property
    def name(self): return "My Custom Rule"

    @property
    def domain(self): return "gst"

    def evaluate(self, data):
        if data.get("field"):
            return self._result("pass", "Check passed")
        return self._result("fail", "Check failed")
```
