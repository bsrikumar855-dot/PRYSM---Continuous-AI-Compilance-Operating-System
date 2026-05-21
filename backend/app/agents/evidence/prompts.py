"""Evidence agent prompts."""

EVIDENCE_MAPPING_PROMPT = """
Map each compliance finding to the specific location in the source document.

OCR Text:
{ocr_text}

Findings:
{findings}

For each finding, identify:
- page_number: Which page contains the evidence
- text_snippet: The exact text that supports the finding
- confidence: How confident the mapping is (0.0-1.0)
"""
