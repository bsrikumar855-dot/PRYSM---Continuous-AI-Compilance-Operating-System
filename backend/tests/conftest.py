"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_invoice_data():
    """Sample extracted invoice data for testing rules."""
    return {
        "invoice_number": "INV-2026-001",
        "invoice_date": "2026-05-14",
        "vendor_name": "Test Corp",
        "total_amount": 11800.0,
        "subtotal": 10000.0,
        "tax_amount": 1800.0,
        "gstin": "29ABCDE1234F1Z5",
        "gst_rate": 18,
    }
