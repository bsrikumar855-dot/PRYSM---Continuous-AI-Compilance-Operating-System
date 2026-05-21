"""OCR text postprocessing."""


class OCRPostProcessor:
    @staticmethod
    def clean(text: str) -> str:
        """Clean and normalize OCR output text."""
        # Remove excessive whitespace, fix common OCR errors
        import re
        text = re.sub(r'\s+', ' ', text).strip()
        return text
