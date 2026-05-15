from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

BASE_DIR = Path(__file__).resolve().parents[4]
PDF_PATH = BASE_DIR / "data" / "samples" / "sample_invoice.pdf"


def test_full_pipeline():

    with open(PDF_PATH, "rb") as f:
        response = client.post(
            "/api/v1/upload",
            files={"file": f}
        )

    assert response.status_code == 200

    data = response.json()

    assert "filename" in data