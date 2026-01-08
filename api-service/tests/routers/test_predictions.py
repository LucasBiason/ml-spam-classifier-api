"""
Unit tests for predictions router.
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_get_model_info(client, classifier_mock):
    """Test GET /api/v1/model/info endpoint."""
    from app.core import lifecycle
    original_classifier = lifecycle.classifier
    lifecycle.classifier = classifier_mock
    # Patch the router's import of classifier from core module
    with patch("app.core.classifier", classifier_mock):
        try:
            response = client.get("/api/v1/model/info")
            assert response.status_code == 200
            data = response.json()
            assert data["loaded"] is True
            assert data["model_type"] == "LogisticRegression"
            assert "accuracy" in data
            assert "precision" in data
            assert "recall" in data
            assert "f1_score" in data
        finally:
            lifecycle.classifier = original_classifier


def test_get_model_info_unloaded(client, classifier_unloaded):
    """Test GET /api/v1/model/info when model is not loaded."""
    from app.core import lifecycle
    original_classifier = lifecycle.classifier
    lifecycle.classifier = classifier_unloaded
    try:
        response = client.get("/api/v1/model/info")
        assert response.status_code == 200
        data = response.json()
        assert data["loaded"] is False
    finally:
        lifecycle.classifier = original_classifier


def test_predict_spam_email(client, classifier_mock):
    """Test POST /api/v1/predict with spam email."""
    from app.core import lifecycle
    original_classifier = lifecycle.classifier
    lifecycle.classifier = classifier_mock
    # Patch the router's import of classifier from core module
    with patch("app.core.classifier", classifier_mock):
        try:
            response = client.post(
                "/api/v1/predict",
                json={"message": "Free money! Click here now to claim your prize!"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["prediction"] == "spam"
            assert data["is_spam"] is True
            assert "confidence" in data
            assert "probability_spam" in data
            assert "probability_ham" in data
            assert "model_info" in data
            assert 0.0 <= data["confidence"] <= 1.0
            assert 0.0 <= data["probability_spam"] <= 1.0
            assert 0.0 <= data["probability_ham"] <= 1.0
        finally:
            lifecycle.classifier = original_classifier


def test_predict_ham_email(client, classifier_mock):
    """Test POST /api/v1/predict with ham email."""
    from app.core import lifecycle
    original_classifier = lifecycle.classifier
    # Mock to return ham - update classes_ and predict_proba
    classifier_mock.model.classes_ = np.array(['ham', 'spam'])
    classifier_mock.model.predict_proba.return_value = np.array([[0.88, 0.12]])  # [ham, spam]
    lifecycle.classifier = classifier_mock
    # Patch the router's import of classifier from core module
    with patch("app.core.classifier", classifier_mock):
        try:
            response = client.post(
                "/api/v1/predict",
                json={"message": "Hi, can we schedule a meeting for tomorrow?"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["prediction"] == "ham"
            assert data["is_spam"] is False
            assert "confidence" in data
            assert "probability_spam" in data
            assert "probability_ham" in data
        finally:
            lifecycle.classifier = original_classifier


def test_predict_missing_message(client):
    """Test POST /api/v1/predict with missing message field."""
    response = client.post("/api/v1/predict", json={})
    assert response.status_code == 422


def test_predict_empty_message(client, classifier_mock):
    """Test POST /api/v1/predict with empty message."""
    from app.core import lifecycle
    original_classifier = lifecycle.classifier
    lifecycle.classifier = classifier_mock
    try:
        response = client.post("/api/v1/predict", json={"message": ""})
        assert response.status_code == 422
    finally:
        lifecycle.classifier = original_classifier


def test_predict_model_not_loaded(client, classifier_unloaded):
    """Test POST /api/v1/predict when model is not loaded."""
    from app.core import lifecycle
    original_classifier = lifecycle.classifier
    lifecycle.classifier = classifier_unloaded
    try:
        response = client.post(
            "/api/v1/predict",
            json={"message": "Test email"}
        )
        assert response.status_code == 503
        assert "not loaded" in response.json()["detail"].lower()
    finally:
        lifecycle.classifier = original_classifier


def test_predict_invalid_json(client):
    """Test POST /api/v1/predict with invalid JSON."""
    response = client.post(
        "/api/v1/predict",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422

