"""Risk agent prompts."""

RISK_SCORING_PROMPT = """
Analyze the following compliance check results and extracted entities.
Identify risk signals, categorize them, and assign severity levels.

Compliance Results:
{compliance_results}

Entities:
{entities}

For each risk, provide:
- risk_level: critical | high | medium | low | info
- category: financial | regulatory | operational | data_quality
- description: Clear explanation of the risk
- recommendation: Actionable remediation step
"""
