"""Extraction prompt templates."""

ENTITY_EXTRACTION_PROMPT = """
You are a financial document entity extraction specialist.
Extract all structured entities from the following document text.

Document Text:
{ocr_text}

Extract the following fields where applicable:
- Invoice number, date, amount, tax details
- GSTIN numbers, HSN codes
- Bank account details, transaction amounts
- Company names, CIN numbers
- TDS certificate details

Return as structured JSON.
"""
