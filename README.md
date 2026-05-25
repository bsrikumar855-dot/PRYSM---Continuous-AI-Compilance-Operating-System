<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:7C3AED,100:F59E0B&height=220&section=header&text=PRYSM&fontSize=72&fontColor=FFFFFF&animation=fadeIn&fontAlignY=38&desc=AI-Powered%20Audit%20Intelligence%20Platform&descAlignY=58&descSize=18" />

<br />

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=26&duration=2800&pause=900&color=F5C542&center=true&vCenter=true&width=900&lines=Know+your+audit+gaps+before+the+auditor+does.;Upload+documents.+Detect+risks.+Generate+audit-ready+reports.;AI+Audit+Intelligence+for+Finance+Teams%2C+CFOs+and+CA+Firms." alt="Typing SVG" />

<br />

<p>
  <img src="https://img.shields.io/badge/Team-Team%20Ragnarok-7C3AED?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Project-PRYSM-F59E0B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Category-AI%20%7C%20FinTech%20%7C%20RegTech-0EA5E9?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Hackathon%20MVP-22C55E?style=for-the-badge" />
</p>

<h3>“Know your audit gaps before the auditor does.”</h3>

<p>
  <b>PRYSM</b> is an AI-powered audit intelligence platform that helps finance teams, CFOs, CA firms, and SMEs detect compliance gaps, reconciliation mismatches, missing invoices, and audit risks before they become expensive problems.
</p>

</div>

---

## 🚀 One-Line Pitch

**PRYSM transforms manual audit preparation from weeks of document checking into minutes of AI-powered compliance intelligence.**

---

## 🧠 Problem Statement

Audit preparation is slow, expensive, and reactive.

Finance teams often spend weeks collecting invoices, GST returns, bank statements, ROC filings, and supporting documents. Critical issues such as GST mismatches, missing invoices, late filings, or unmatched bank entries are usually discovered too late — during the audit itself.

This leads to:

- Delayed audit readiness
- High CA preparation costs
- Missed compliance gaps
- Penalties and interest exposure
- Poor document traceability
- Last-minute finance team stress

> Businesses should not discover audit risks only when the auditor arrives.

---

## 💡 Solution Overview

**PRYSM** acts as a continuous audit intelligence layer.

Users upload financial documents. PRYSM extracts structured entities using OCR and LLMs, runs deterministic compliance checks, detects gaps, explains risks in plain English, and generates a professional audit-ready PDF report.

```mermaid
flowchart LR
    A[Upload Financial Documents] --> B[OCR + PDF Text Extraction]
    B --> C[LLM Entity Extraction]
    C --> D[Structured Data Store]
    D --> E[Compliance Rule Engine]
    E --> F[Risk Dashboard]
    F --> G[Audit-Ready PDF Report]
    F --> H[AI Copilot Explanations]
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📤 AI Document Upload Portal | Upload invoices, GST returns, bank statements, ROC filings, and scanned PDFs |
| 🔍 PDF + OCR Extraction | Uses PyMuPDF and Tesseract to extract text from native and scanned documents |
| 🧠 LLM Entity Extraction | Extracts GSTIN, invoice number, dates, amounts, HSN codes, vendor names, and tax details |
| ⚖️ Compliance Rule Engine | Runs 18 deterministic audit and compliance rules |
| 🧾 GST Mismatch Detection | Compares invoice data, GST returns, and extracted values |
| 🚨 Missing Invoice Detection | Detects invoice sequence gaps and missing financial records |
| 📊 Risk Dashboard | Displays Critical, High, Medium, and Low severity findings |
| 🤖 AI Copilot | Explains every risk in plain English for CFOs, founders, and finance teams |
| 📑 Audit PDF Reports | Generates CA-ready audit reports with evidence and remediation steps |
| 🧬 ChromaDB Search | Enables semantic search and document intelligence across uploaded files |

---

## 🛠️ Tech Stack

<div align="center">

### Frontend

<img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
<img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
<img src="https://img.shields.io/badge/Tailwind%20CSS-0F172A?style=for-the-badge&logo=tailwindcss&logoColor=38BDF8" />

### Backend

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Python-111827?style=for-the-badge&logo=python&logoColor=FFD43B" />
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/PostgreSQL-1E3A8A?style=for-the-badge&logo=postgresql&logoColor=white" />

### AI + Document Intelligence

<img src="https://img.shields.io/badge/Groq-FF6B00?style=for-the-badge&logo=groq&logoColor=white" />
<img src="https://img.shields.io/badge/LLaMA-111827?style=for-the-badge&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/PyMuPDF-16A34A?style=for-the-badge" />
<img src="https://img.shields.io/badge/Tesseract%20OCR-2563EB?style=for-the-badge" />
<img src="https://img.shields.io/badge/ChromaDB-7C3AED?style=for-the-badge" />

### Deployment

<img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />

</div>

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    U[User Browser] --> FE[React / Next.js Frontend]

    FE -->|REST API| API[FastAPI Backend]

    API --> UPLOAD[Upload Service]
    API --> EXTRACT[Extraction Service]
    API --> ANALYZE[Compliance Analyzer]
    API --> REPORT[Report Generator]
    API --> COPILOT[AI Copilot API]

    UPLOAD --> DOCS[(Uploaded Documents)]

    EXTRACT --> PDF[PyMuPDF Parser]
    EXTRACT --> OCR[Tesseract OCR]
    PDF --> LLM[Groq / LLaMA Entity Extraction]
    OCR --> LLM

    LLM --> DB[(SQLite / PostgreSQL)]
    LLM --> VECTOR[(ChromaDB Vector Store)]

    DB --> RULES[18 Compliance Rules]
    VECTOR --> COPILOT

    RULES --> RISKS[Risk Scoring Engine]
    RISKS --> DASH[Risk Dashboard]
    RISKS --> REPORT

    REPORT --> PDFOUT[Audit-Ready PDF]
```

---

## 🔄 PRYSM Workflow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant OCR
    participant LLM
    participant Rules
    participant Report

    User->>Frontend: Upload financial documents
    Frontend->>Backend: POST /upload
    Backend->>OCR: Extract text from PDFs/images
    OCR->>LLM: Send cleaned document text
    LLM->>Backend: Return structured entities
    Backend->>Rules: Run compliance checks
    Rules->>Backend: Return risk findings
    Backend->>Frontend: Display dashboard
    User->>Frontend: Click Export Report
    Frontend->>Report: Generate audit PDF
    Report->>User: Download CA-ready report
```

---

## 🎬 Demo Preview

> Replace these placeholders with your actual project GIFs/screenshots.

| Landing Page | Risk Dashboard |
|---|---|
| ![Landing Demo](https://placehold.co/600x350/0F172A/F5C542?text=PRYSM+Landing+Page) | ![Dashboard Demo](https://placehold.co/600x350/111827/EF4444?text=Risk+Dashboard) |

| AI Extraction | Audit Report |
|---|---|
| ![Extraction Demo](https://placehold.co/600x350/111827/38BDF8?text=AI+Entity+Extraction) | ![Report Demo](https://placehold.co/600x350/111827/22C55E?text=Audit+PDF+Report) |

---

## ⚙️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/prysm.git
cd prysm
```

---

## 🧩 Backend Setup

```bash
cd backend
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will run on:

```bash
http://localhost:8000
```

API docs will be available at:

```bash
http://localhost:8000/docs
```

---

## 🎨 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on:

```bash
http://localhost:3000
```

---

## 🔐 Environment Variables

Create a `.env` file inside the backend folder:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///./prysm.db
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIR=./uploads
REPORT_DIR=./reports
```

Create a `.env.local` file inside the frontend folder:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check backend server health |
| `POST` | `/upload` | Upload financial documents |
| `POST` | `/extract` | Extract text and entities from uploaded documents |
| `POST` | `/analyze` | Run compliance rules and generate risks |
| `GET` | `/risks/{doc_id}` | Fetch risk findings for a document |
| `POST` | `/copilot` | Ask AI Copilot questions about audit risks |
| `GET` | `/report/{doc_id}` | Generate and download audit-ready PDF report |

---

## 📁 Project Structure

```bash
PRYSM/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── upload.py
│   │   │   ├── extract.py
│   │   │   ├── analyze.py
│   │   │   ├── risks.py
│   │   │   └── report.py
│   │   │
│   │   ├── services/
│   │   │   ├── pdf_parser.py
│   │   │   ├── ocr_service.py
│   │   │   ├── llm_extractor.py
│   │   │   ├── compliance_engine.py
│   │   │   ├── risk_scoring.py
│   │   │   └── report_generator.py
│   │   │
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   ├── entity.py
│   │   │   └── risk.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   │
│   │   └── rules/
│   │       └── rules.json
│   │
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── app/
│   ├── components/
│   │   ├── UploadPortal.tsx
│   │   ├── RiskDashboard.tsx
│   │   ├── RiskCard.tsx
│   │   ├── CopilotPanel.tsx
│   │   └── ReportViewer.tsx
│   │
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── api-contract.md
│   └── demo-script.md
│
├── tests/
│   ├── backend/
│   └── frontend/
│
└── README.md
```

---

## 🧪 Demo Flow for Judges

```mermaid
flowchart LR
    A[1. Open PRYSM Landing Page] --> B[2. Upload Sample Documents]
    B --> C[3. Watch AI Extract Entities]
    C --> D[4. Risk Dashboard Loads]
    D --> E[5. Click Critical Risk]
    E --> F[6. View Plain-English Explanation]
    F --> G[7. Export Audit PDF]
    G --> H[8. Judges See Audit Readiness in Minutes]
```

### Judge Demo Script

| Step | Action | What Judges See |
|---|---|---|
| 1 | Open PRYSM | Premium fintech-style landing page |
| 2 | Upload documents | Invoice, GST return, bank statement upload |
| 3 | Run extraction | GSTIN, invoice number, dates, amounts appear |
| 4 | View dashboard | Critical and High risks highlighted |
| 5 | Open risk details | Evidence, explanation, and remediation steps |
| 6 | Ask AI Copilot | Plain-English answer about the compliance issue |
| 7 | Export report | Professional audit-ready PDF download |
| 8 | Closing line | “Know your audit gaps before the auditor does.” |

---

## 👥 Team Ragnarok

| Member | Role | Responsibility |
|---|---|---|
| **Shreekumar** | Team Lead / System Architect | Architecture, integration, backend design, demo strategy |
| **Santheesh** | Backend Lead | FastAPI, OCR pipeline, database, compliance engine |
| **Tharun BL** | Frontend Lead | React / Next.js UI, dashboard, upload portal, UX |
| **Vishal** | Research Lead | GST rules, compliance logic, prompt engineering |
| **Sharun** | Testing & CI/CD Lead | Testing, deployment, QA, CI/CD pipeline |

---

## 🛣️ Roadmap

```mermaid
timeline
    title PRYSM Product Roadmap

    Hackathon MVP
        : Upload documents
        : OCR extraction
        : LLM entity extraction
        : 18 compliance rules
        : Risk dashboard
        : Audit PDF export

    Phase 2
        : Continuous monitoring
        : Daily reconciliation
        : Audit readiness score
        : GSTN API integration

    Phase 3
        : Human review workflow
        : CA firm mode
        : Evidence tracking
        : Tally and Zoho integration

    Phase 4
        : AI Copilot
        : Vendor risk scoring
        : Fraud indicators
        : Predictive compliance

    Phase 5
        : Multi-tenant SaaS
        : Enterprise security
        : SSO and RBAC
        : Global compliance packs
```

---

## 🧠 Future Enhancements

- Multi-agent audit workflow
- Human-in-the-loop compliance review
- Tally and Zoho Books integration
- GSTN API integration
- Vendor risk scoring
- Fraud pattern detection
- Multi-client CA firm dashboard
- Enterprise RBAC and SSO
- Continuous audit readiness monitoring
- Predictive compliance alerts

---

## 🏆 Why PRYSM Stands Out

PRYSM is not just another document parser.

It combines:

- **AI extraction** for speed
- **Deterministic rules** for trust
- **Risk scoring** for prioritization
- **Plain-English explanations** for clarity
- **Audit-ready reports** for real-world usability

> PRYSM does not replace auditors.  
> It makes every finance team audit-ready before the auditor arrives.

---

## 📜 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Team Ragnarok

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
```

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:F59E0B,50:7C3AED,100:0F172A&height=140&section=footer" />

<h2>PRYSM</h2>

<h3>Know your audit gaps before the auditor does.</h3>

<p>
  <b>Built with dedication by Team Ragnarok.</b>
</p>

</div>
