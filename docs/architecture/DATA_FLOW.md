# PRYSM — Data Flow

## Ingestion Pipeline
1. **Upload** → File saved to disk, metadata to DB
2. **OCR** → PyMuPDF → PaddleOCR → OpenCV preprocessing
3. **Extraction** → ExtractionAgent (LLM) → structured entities
4. **Compliance** → ComplianceAgent → Rule Engine (deterministic)
5. **Risk** → RiskAgent → risk flags & scoring
6. **Evidence** → EvidenceAgent → source document linking
7. **Review** → Human review queue (if failures detected)
8. **Report** → ReportingAgent → PDF generation
