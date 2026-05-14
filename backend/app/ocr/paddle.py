"""PaddleOCR adapter."""


class PaddleOCRExtractor:
    def extract(self, file_path: str) -> dict:
        """Extract text using PaddleOCR for scanned documents."""
        # TODO: Implement with PaddleOCR
        return {"text": "", "boxes": [], "confidence": 0.0}
