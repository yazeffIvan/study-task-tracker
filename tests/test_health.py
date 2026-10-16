from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "Трекер учебных задач" in response.text
