from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_tests():
    response = client.get("/api/tests")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_create_execution():
    response = client.post("/api/executions", json={"suite": "Dashboard"})
    assert response.status_code == 201
    assert response.json()["status"] == "queued"
    assert response.json()["total"] >= 1


