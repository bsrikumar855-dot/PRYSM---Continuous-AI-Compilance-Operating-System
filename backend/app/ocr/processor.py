"""Unified OCR processor — orchestrates OCR pipeline."""


class OCRProcessor:
    """Orchestrates the OCR pipeline: PyMuPDF → PaddleOCR → OpenCV."""

    async def process(self, file_path: str) -> dict:
        """Process a document through the OCR pipeline.

        Returns:
            dict with keys: text, pages, page_count, confidence
        """
        # Step 1: Try PyMuPDF for text extraction
        # Step 2: If low confidence, use PaddleOCR
        # Step 3: Apply OpenCV preprocessing if needed
        # Step 4: Post-process text
        return {"text": "", "pages": [], "page_count": 0, "confidence": 0.0}
