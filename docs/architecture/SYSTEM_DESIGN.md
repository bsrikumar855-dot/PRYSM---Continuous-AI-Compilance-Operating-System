# PRYSM — System Design

## Architecture Pattern
Modular Monolith — all components in a single deployable unit with clean module boundaries.

## Data Flow
```
Document Upload → OCR Pipeline → AI Extraction → Compliance Engine → Risk Scoring → Human Review → Report Generation
```

## Layer Separation
- **Routers**: HTTP only, no business logic
- **Services**: Business logic orchestration
- **Repositories**: Data access (SQL queries)
- **Agents**: AI-powered processing
- **Engine**: Deterministic rule execution
- **Workflows**: Multi-step pipeline coordination
