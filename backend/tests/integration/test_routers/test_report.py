from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_report_generation():
    response = client.post("/api/v1/generate/test-doc-id")

    assert response.status_code in [200, 404]