"""
Unit tests for prediction controller.
"""

import pytest
from fastapi import HTTPException, status

from app.controllers.prediction_controller import PredictionController


def test_get_model_info_success(classifier_mock):
    """Test get_model_info with loaded model."""
    result = PredictionController.get_model_info(classifier_mock)
    assert result["loaded"] is True
    assert result["model_type"] == "LogisticRegression"
    assert result["accuracy"] == 0.98
    assert result["precision"] == 0.97
    assert result["recall"] == 0.96
    assert result["f1_score"] == 0.965


def test_get_model_info_unloaded(classifier_unloaded):
    """Test get_model_info with unloaded model."""
    result = PredictionController.get_model_info(classifier_unloaded)
    assert result["loaded"] is False
    assert "model_type" not in result or result.get("model_type") is None
    assert "accuracy" not in result or result.get("accuracy") is None


def test_classify_email_spam(classifier_mock):
    """Test classify_email with spam email."""
    email_data = {"message": "Free money! Click here now!"}
    result = PredictionController.classify_email(classifier_mock, email_data)
    assert isinstance(result, dict)
    assert result["prediction"] == "spam"
    assert result["is_spam"] is True
    assert "confidence" in result
    assert "probability_spam" in result
    assert "probability_ham" in result
    assert "model_info" in result


def test_classify_email_ham(classifier_mock):
    """Test classify_email with ham email."""
    # Mock to return ham
    classifier_mock.model.predict.return_value = [0]
    classifier_mock.model.predict_proba.return_value = [[0.85, 0.15]]
    
    email_data = {"message": "Hi, how are you?"}
    result = PredictionController.classify_email(classifier_mock, email_data)
    assert isinstance(result, dict)
    assert result["prediction"] == "ham"
    assert result["is_spam"] is False
    assert result["confidence"] > 0.5


def test_classify_email_model_not_loaded(classifier_unloaded):
    """Test classify_email raises HTTPException when model is not loaded."""
    email_data = {"message": "Test email"}
    with pytest.raises(HTTPException) as exc_info:
        PredictionController.classify_email(classifier_unloaded, email_data)
    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


def test_classify_email_empty_message(classifier_mock):
    """Test classify_email with empty message."""
    email_data = {"message": ""}
    with pytest.raises(HTTPException) as exc_info:
        PredictionController.classify_email(classifier_mock, email_data)
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


def test_classify_email_exception_handling(classifier_mock):
    """Test classify_email handles exceptions gracefully."""
    from unittest.mock import patch
    
    with patch.object(classifier_mock, 'classify', side_effect=Exception("Model error")):
        email_data = {"message": "Test email"}
        with pytest.raises(HTTPException) as exc_info:
            PredictionController.classify_email(classifier_mock, email_data)
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
