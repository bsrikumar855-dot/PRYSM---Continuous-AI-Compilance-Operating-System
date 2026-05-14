# PRYSM API Reference

Base URL: `http://localhost:8000/api/v1`

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/documents/upload` | Upload document |
| GET | `/documents/` | List documents |
| GET | `/documents/{id}` | Get document |
| POST | `/compliance/run/{id}` | Run compliance check |
| GET | `/compliance/results/{id}` | Get results |
| GET | `/risk/overview` | Risk dashboard |
| GET | `/risk/flags/{id}` | Document risk flags |
| GET | `/review/queue` | Review queue |
| POST | `/review/tasks/{id}/approve` | Approve review |
| POST | `/reports/generate/{id}` | Generate report |
| GET | `/reports/{id}/download` | Download PDF |
| POST | `/copilot/chat` | Copilot chat |
