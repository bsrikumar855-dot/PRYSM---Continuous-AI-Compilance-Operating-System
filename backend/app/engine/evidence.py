"""Evidence mapping — links rule results to source document evidence."""



class EvidenceMapper:
    """Maps compliance results to their source evidence in documents."""

    @staticmethod
    def map_evidence(rule_result: dict, ocr_text: str) -> dict:
        """Find evidence in OCR text that supports a rule result."""
        # TODO: Text search / highlighting logic
        return {
            "rule_id": rule_result.get("rule_id"),
            "evidence_text": "",
            "page": None,
            "confidence": 0.0,
        }
