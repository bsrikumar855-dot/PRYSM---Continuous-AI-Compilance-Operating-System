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
│   └── src/
│       ├── app/       # Pages (App Router)
│       ├── components/# UI components
│       ├── services/  # API client
│       └── ...
├── docs/              # Documentation
├── data/              # Sample & seed data
├── scripts/           # Dev & ops scripts
└── .github/           # CI/CD workflows
```

## ⚡ Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
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