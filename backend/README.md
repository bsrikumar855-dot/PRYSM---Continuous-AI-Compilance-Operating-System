# PRYSM Backend

Simple, stable, demo-ready FastAPI backend for the PRYSM Continuous AI Compliance Operating System.

## Setup

```bash
cd backend
python -m pip install -r requirements.txt
```

## Run

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

## Swagger UI

Open: http://127.0.0.1:8001/docs

## LLM Environment

Set these in the project root `.env`:

```env
GROQ_API_KEY=your-groq-api-key
LLM_MODEL=llama-3.3-70b-versatile
LLM_FALLBACK_MODEL=gemma-4-26b
```

The backend exposes the active primary/fallback model names in `/health` without exposing the API key.
The Copilot endpoint sends multi-turn conversation history and a compact live workspace snapshot to the
configured Groq chat model. If the model service is temporarily unavailable, PRYSM falls back to local
audit guidance instead of failing the session.

## Frontend Environment

Set in `frontend/PRYSM-Fr-main/PRYSM-Fr-main/.env.local`:

```
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /api/v1/upload | Upload documents |
| GET | /api/v1/ | List all documents |
| GET | /api/v1/{document_id} | Get single document |
| DELETE | /api/v1/{document_id} | Delete document |
| GET | /api/v1/overview | Risk overview dashboard |
| GET | /api/v1/flags/{document_id} | Get flags for document |
| GET | /api/v1/reports/ | List all reports |
| GET | /api/v1/reports/{report_id} | Get single report |
| POST | /api/v1/reports/generate/{document_id} | Generate report |
| POST | /api/v1/reports/generate | Generate branded audit-session PDF and LaTeX source |
| GET | /api/v1/reports/{report_id}/download | Download report |
| GET | /api/v1/documents/{document_id}/file | View/download uploaded source evidence |
| POST | /api/v1/documents/{document_id}/reprocess | Re-run extraction from source evidence |

## PDF Reports

The Reports page can generate an audit-session PDF from eligible documents and active risk flags.
Each generated PDF is backed by a branded LaTeX `.tex` source with PRYSM color styling. If
`xelatex` or `pdflatex` is installed, the backend compiles that source directly; otherwise it
renders an equivalent PDF immediately while retaining the LaTeX source for later compilation.
Uploaded evidence is scoped to the active audit session by default. Files are stored under `UPLOAD_DIR`, but are not automatically reloaded into a fresh server session; set `RESTORE_UPLOADS_ON_STARTUP=true` only when intentionally continuing the same evidence set.
