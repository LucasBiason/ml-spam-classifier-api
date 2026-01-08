"""
Pytest configuration and shared fixtures.
"""

from unittest.mock import MagicMock, Mock

import numpy as np
import pytest

from app.models.spam_classifier import SpamClassifier


@pytest.fixture
def mock_model():
    """Create a mock classification model."""
    model = MagicMock()
    model.predict.return_value = np.array([1])  # 1 = spam
    model.predict_proba.return_value = np.array([[0.05, 0.95]])  # [ham, spam]
    model.classes_ = np.array(['ham', 'spam'])  # Required for classify method
    return model


@pytest.fixture
def mock_vectorizer():
    """Create a mock TF-IDF vectorizer."""
    vectorizer = Mock()
    vectorizer.transform.return_value = np.array([[0.1, 0.2, 0.3]])
    return vectorizer


@pytest.fixture
def mock_metadata():
    """Create mock model metadata."""
    return {
        "model_type": "LogisticRegression",
        "training_samples": 5172,
        "optimization_accuracy": 0.98,
        "optimization_precision": 0.97,
        "optimization_recall": 0.96,
        "optimization_f1": 0.965,
        "trained_date": "2024-01-15",
    }


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {"message": "Free money! Click here now to claim your prize!"}


@pytest.fixture
def classifier_mock(mock_model, mock_vectorizer, mock_metadata):
    """Create a SpamClassifier instance with mocked dependencies."""
    classifier = SpamClassifier(models_dir="tests/fixtures/models")
    classifier.model = mock_model
    classifier.vectorizer = mock_vectorizer
    classifier.metadata = mock_metadata
    classifier.is_loaded = True
    return classifier


@pytest.fixture
def classifier_unloaded():
    """Create an unloaded SpamClassifier instance."""
    classifier = SpamClassifier(models_dir="tests/fixtures/models")
    classifier.is_loaded = False
    return classifier





