.PHONY: dev backend frontend test lint clean

# Start everything
dev:
	@echo "Starting PRYSM development servers..."
	make backend & make frontend

# Backend
backend:
	cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

# Frontend
frontend:
	cd frontend/PRYSM-Fr-main/PRYSM-Fr-main && npm run dev

# Tests
test:
	cd backend && python -m pytest tests/ -v

test-cov:
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=html

# Lint
lint:
	cd backend && ruff check app/

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
