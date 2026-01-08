"""
Unit tests for main FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_app_initialization():
    """Test FastAPI app is properly initialized."""
    assert app.title == "ML Spam Classifier API"
    assert app.version == "1.0.0"
    assert app.docs_url == "/docs"
    assert app.redoc_url == "/redoc"


def test_cors_middleware():
    """Test CORS middleware is configured."""
    middleware_classes = [m.cls.__name__ for m in app.user_middleware]
    assert "CORSMiddleware" in middleware_classes


def test_routers_included(client):
    """Test routers are included."""
    # Test health router
    response = client.get("/health")
    assert response.status_code == 200

    # Test predictions router
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200


def test_openapi_schema(client):
    """Test OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "ML Spam Classifier API"
    assert schema["info"]["version"] == "1.0.0"


def test_docs_endpoint(client):
    """Test Swagger UI docs endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint(client):
    """Test ReDoc endpoint."""
    response = client.get("/redoc")
    assert response.status_code == 200





