"""Compliance agent prompts."""

COMPLIANCE_MAPPING_PROMPT = """
Given the extracted entities below, map them to compliance rule inputs.

Entities:
{entities}

For each entity, determine:
1. Which compliance domain applies (GST, Invoice, Bank, ROC, TDS)
2. The specific fields needed for rule validation
3. Any cross-reference checks required

Return structured JSON mapping.
"""
