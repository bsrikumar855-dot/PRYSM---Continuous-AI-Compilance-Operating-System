# 🔱 PRYSM — Continuous AI Compliance Operating System

> **Team Ragnarok** | Enterprise-Grade AI-Powered Compliance Platform

[![CI](https://github.com/bsrikumar855-dot/PRYSM---Continuous-AI-Compilance-Operating-System/actions/workflows/ci.yml/badge.svg)](https://github.com/bsrikumar855-dot/PRYSM---Continuous-AI-Compilance-Operating-System/actions)

---

## 🚀 What is PRYSM?

PRYSM is an AI-powered Continuous Compliance Operating System that automates document analysis, compliance verification, risk assessment, and audit reporting for financial documents.

**Core Workflow:**
```
Upload → OCR → AI Extraction → Compliance Engine → Risk Scoring → Human Review → Audit Reports
```

## 🏗️ Architecture

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js + Tailwind + shadcn/ui | Enterprise dashboard |
| Backend | FastAPI (Python) | API & business logic |
| OCR | PyMuPDF + PaddleOCR + OpenCV | Document parsing |
| AI | Groq + LLaMA 3.3 | Entity extraction & analysis |
| Database | PostgreSQL / SQLite | Data persistence |
| Vector DB | ChromaDB / pgvector | Semantic search |
| Reports | ReportLab | PDF audit reports |

## 📂 Project Structure

```
PRYSM/
├── backend/           # FastAPI application
│   └── app/
│       ├── routers/   # API endpoints
│       ├── services/  # Business logic
│       ├── agents/    # AI agent layer
│       ├── engine/    # Deterministic compliance rules
│       ├── ocr/       # Document parsing
│       └── ...
├── frontend/          # Next.js application
│   └── PRYSM-Fr-main/
│       └── PRYSM-Fr-main/
│           ├── src/
│           ├── public/
│           └── package.json
├── docs/              # Documentation
├── data/              # Sample & seed data
├── scripts/           # Dev & ops scripts
└── .github/           # CI/CD workflows
```

## ⚡ Quick Start

## Run Full Stack Locally

### Backend
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### Frontend
```bash
cd frontend/PRYSM-Fr-main/PRYSM-Fr-main
npm install
npm run dev
```

Backend runs at `http://127.0.0.1:8001`. Frontend runs at `http://localhost:3000`.

Set the frontend API base URL in `frontend/PRYSM-Fr-main/PRYSM-Fr-main/.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001
```

Backend endpoints used by the frontend:

```text
GET    /health
POST   /api/v1/upload
GET    /api/v1/
GET    /api/v1/{document_id}
DELETE /api/v1/{document_id}
GET    /api/v1/overview
GET    /api/v1/flags/{document_id}
GET    /api/v1/reports/
GET    /api/v1/reports/{report_id}
POST   /api/v1/reports/generate/{document_id}
GET    /api/v1/reports/{report_id}/download
```

## 🧪 Testing
```bash
cd backend
python -m pytest tests/ -v
```

## 📖 Documentation
- [System Design](docs/architecture/SYSTEM_DESIGN.md)
- [Data Flow](docs/architecture/DATA_FLOW.md)
- [Agent Design](docs/architecture/AGENT_DESIGN.md)
- [API Reference](docs/api/API_REFERENCE.md)
- [Rule Authoring](docs/rules/RULE_AUTHORING.md)
- [Development Setup](docs/setup/DEVELOPMENT.md)

## 📄 License
MIT License — see [LICENSE](LICENSE)
