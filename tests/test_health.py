"""Tests for health check endpoints."""


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_shape(client):
    data = client.get("/health").json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert "uptime_seconds" in data
    assert "environment" in data


def test_health_uptime_is_non_negative(client):
    data = client.get("/health").json()
    assert data["uptime_seconds"] >= 0


def test_liveness_returns_200(client):
    response = client.get("/health/live")
    assert response.status_code == 200


def test_liveness_response(client):
    data = client.get("/health/live").json()
    assert data["status"] == "alive"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()
    assert "docs" in response.json()
