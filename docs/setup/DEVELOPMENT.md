# PRYSM Development Setup

## Prerequisites
- Python 3.11+
- Node.js 20+
- Git

## Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Running Tests
```bash
cd backend
python -m pytest tests/ -v
```
