# PRYSM — Agent Design

## Principles
- Agents are **logical** (in-process), not distributed services
- All agents share a common `AgentContext` dataclass
- Orchestrator manages sequencing; agents never call each other directly
- Each agent has: `agent.py`, `prompts.py`, optional `parsers.py`

## Agents
| Agent | Purpose |
|---|---|
| ExtractionAgent | Extracts structured entities from OCR text |
| ComplianceAgent | Maps entities to rule engine inputs |
| RiskAgent | Scores and categorizes risk signals |
| EvidenceAgent | Links findings to source document evidence |
| ReportingAgent | Generates narrative summaries for reports |
| CopilotAgent | Interactive Q&A over compliance data |
