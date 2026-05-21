"""Reporting agent prompts."""

REPORT_NARRATIVE_PROMPT = """
Generate a professional audit report narrative based on the following data.

Compliance Results: {compliance_results}
Risk Flags: {risk_flags}
Evidence Map: {evidence_map}

Sections to generate:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Risk Assessment (categorized by severity)
4. Recommendations (actionable steps)
5. Conclusion
"""
