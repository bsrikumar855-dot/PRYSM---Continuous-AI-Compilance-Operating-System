<div align="center">

# ⚡ AHAL V2

### AI-powered ingestion, analysis, and intelligence engine for large codebases

![Python](https://img.shields.io/badge/Python-87.6%25-blue?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-12%25-3178C6?style=for-the-badge&logo=typescript)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey?style=for-the-badge)

<br />

**AHAL V2** is a full-stack AI ingestion engine designed to upload, scan, analyze, and extract intelligence from repositories, files, and codebases.

> Built for fast analysis, structured outputs, API-first workflows, and developer-friendly automation.

</div>

---

## 🚀 Overview

AHAL V2 is a modern AI-powered codebase analysis platform.  
It provides a **FastAPI backend**, a **React + Vite frontend**, Docker support, session-based analysis, health monitoring, GitHub webhook support, and optional LLM-powered intelligence using Gemini-compatible configuration.

The project is structured for developers who want to inspect large codebases, upload project files, track scan sessions, and generate useful intelligence through API endpoints.

---

## ✨ Key Features

- ⚡ **FastAPI backend** for high-performance API workflows
- 📁 **File upload and ingestion pipeline**
- 🧠 **Optional LLM-powered analysis**
- 🔎 **Repository/codebase scanning support**
- 🧾 **Session-based analysis tracking**
- 📊 **Health and metrics endpoints**
- 🔗 **GitHub webhook integration**
- 🖥️ **React + Vite frontend**
- 🎨 **Tailwind CSS based UI**
- 🐳 **Docker and Docker Compose support**
- 🧪 **Pytest testing setup**
- 🛠️ **Makefile shortcuts for development**
- 🌱 **Environment-based configuration**
- 🗄️ **Memory storage by default with MongoDB option**

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Uvicorn, Pydantic |
| Frontend | React, TypeScript, Vite |
| Styling | Tailwind CSS |
| Animation/UI | Framer Motion, Lucide React |
| Testing | Pytest |
| DevOps | Docker, Docker Compose, Makefile |
| Storage | Memory backend, optional MongoDB |
| AI/LLM | Gemini-compatible configuration |
| PDF/Reports | fpdf2 |

---

## 📂 Project Structure

```txt
AHAL-V2/
├── app/                    # FastAPI backend application
│   ├── api/                # API routers
│   ├── chat/               # Chat / intent routing logic
│   ├── config.py           # App configuration
│   ├── main.py             # FastAPI entry point
│   ├── sessions/           # Session management
│   └── webhooks/           # GitHub webhook routes
│
├── frontend/               # React + Vite frontend
│   ├── src/                # Frontend source code
│   ├── package.json        # Frontend dependencies and scripts
│   └── vite.config.*       # Vite configuration
│
├── docs/                   # Project documentation
├── scripts/                # Utility scripts
├── tests/                  # Backend tests
│
├── .env.example            # Environment variable template
├── Dockerfile              # Backend Docker image
├── docker-compose.yml      # API + optional MongoDB setup
├── Makefile                # Common dev commands
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Runtime Python dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md               # Project documentation
