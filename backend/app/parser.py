"""Document parser for PRYSM backend.

Extracts text from PDFs/images and parses structured fields using regex.
Never crashes; returns UNKNOWN for missing fields.
"""

import re
from importlib import import_module


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text from a file. Returns empty string on failure."""
    lower = filename.lower()

    if lower.endswith(".pdf"):
        return _extract_pdf(file_bytes)

    if lower.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
        return _extract_image(file_bytes)

    if lower.endswith((".txt", ".csv", ".json", ".md")):
        return _decode_text(file_bytes)

    return ""


def _extract_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF."""
    try:
        fitz = import_module("fitz")

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = [page.get_text() for page in doc]
        doc.close()
        return "\n".join(text_parts).strip()
    except Exception:
        return ""


def _extract_image(file_bytes: bytes) -> str:
    """Try OCR on image. Returns empty string if OCR dependencies are missing."""
    try:
        import io

        pytesseract = import_module("pytesseract")
        image_module = import_module("PIL.Image")

        image = image_module.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image).strip()
    except Exception:
        return ""


def _decode_text(file_bytes: bytes) -> str:
    """Decode text-like files without raising Unicode errors."""
    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return file_bytes.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return ""


def classify_document(text: str) -> str:
    """Classify the document type based on text content."""
    lower = text.lower()

    if any(keyword in lower for keyword in ["audit report", "auditor's report", "auditors' report", "independent auditor", "audit readiness"]):
        return "audit_report"
    if any(keyword in lower for keyword in ["gstr", "gst return", "taxable value"]):
        return "gst_return"
    if "bank statement" in lower:
        return "bank_statement"
    if re.search(r"\b(?:tax\s+invoice|invoice\s*(?:no|number|#|num)\b)", lower):
        return "invoice"

    return "unknown"


def parse_document(text: str) -> dict:
    """Parse structured fields from document text using regex."""
    doc_type = classify_document(text)

    invoice_number = _extract_invoice_number(text)
    vendor_name = _extract_vendor_name(text)

    if doc_type not in ("invoice", "unknown"):
        invoice_number = "NOT_APPLICABLE"
        vendor_name = "NOT_APPLICABLE"

    return {
        "document_type": doc_type,
        "amount": _extract_amount(text),
        "date": _extract_date(text),
        "gstin": _extract_gstin(text),
        "invoice_number": invoice_number,
        "vendor_name": vendor_name,
    }


def _extract_gstin(text: str) -> str:
    """Extract GSTIN, the 15-character Indian tax ID."""
    match = re.search(r"\b\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z][A-Z0-9]\b", text, re.IGNORECASE)
    return match.group(0).upper() if match else "UNKNOWN"


def _extract_date(text: str) -> str:
    """Extract a date in common formats."""
    patterns = [
        r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
        r"\b\d{4}[/-]\d{2}[/-]\d{2}\b",
        r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return "UNKNOWN"


def _extract_amount(text: str) -> str:
    """Extract a monetary amount."""
    patterns = [
        r"(?:Rs\.?|INR|\u20b9)\s*([\d,]+(?:\.\d{1,2})?)",
        r"(?:total|amount|grand total|net amount)[:\s]*(?:Rs\.?|INR|\u20b9)?\s*([\d,]+(?:\.\d{1,2})?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(1).replace(",", "").strip()
            if any(character.isdigit() for character in amount):
                return amount
    return "UNKNOWN"


def _extract_invoice_number(text: str) -> str:
    """Extract an invoice number."""
    patterns = [
        r"(?:invoice\s*(?:no|number|#|num))[.:\s]*([\w\-/]+)",
        r"(?:inv\s*(?:no|#))[.:\s]*([\w\-/]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "UNKNOWN"


def _extract_vendor_name(text: str) -> str:
    """Extract a vendor/company name using a first-line heuristic."""
    patterns = [
        r"(?:vendor|supplier|company|from|seller)[:\s]+(.+)",
        r"(?:M/s\.?|Messrs\.?)\s+(.+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            name = re.split(r"[,\n\r]", name)[0].strip()
            if len(name) > 2:
                return name
    return "UNKNOWN"
