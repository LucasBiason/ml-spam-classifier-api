"""
Unit tests for SpamClassifier model.
"""

import pytest
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import joblib
import os

from app.models.spam_classifier import SpamClassifier


def test_classifier_initialization():
    """Test SpamClassifier initialization."""
    classifier = SpamClassifier(models_dir="tests/fixtures/models")
    assert str(classifier.models_dir) == "tests/fixtures/models"
    assert classifier.model is None
    assert classifier.vectorizer is None
    assert classifier.metadata is None
    assert classifier.is_loaded is False


def test_load_model_success():
    """Test load_model when files exist."""
    with patch("joblib.load") as mock_load:
        mock_model = MagicMock()
        mock_vectorizer = MagicMock()
        mock_metadata = {"model_type": "LogisticRegression"}
        
        load_calls = []
        def load_side_effect(path):
            path_str = str(path)
            load_calls.append(path_str)
            if "best_model_temp" in path_str:
                return mock_model
            elif "tfidf_vectorizer" in path_str:
                return mock_vectorizer
            elif "metadata" in path_str:
                return mock_metadata
            return None
        
        mock_load.side_effect = load_side_effect
        
        # Mock Path.exists - patch at the instance level
        # Path.exists() is called on instances, so side_effect receives self as first arg
        with patch.object(Path, "exists", autospec=True) as mock_exists:
            def exists_side_effect(path_instance):
                path_str = str(path_instance)
                # Return True for metadata, False for label_encoder (not present in this test)
                if "label_encoder" in path_str:
                    return False
                # Check if it's one of the files we want to exist
                if "best_model_temp" in path_str or "tfidf_vectorizer" in path_str or "metadata" in path_str:
                    return True
                return False
            mock_exists.side_effect = exists_side_effect
            
            classifier = SpamClassifier(models_dir="tests/fixtures/models")
            classifier.load()
        
        assert classifier.model == mock_model
        assert classifier.vectorizer == mock_vectorizer
        assert classifier.metadata == mock_metadata
        assert classifier.is_loaded is True


def test_load_model_file_not_found():
    """Test load_model when model files don't exist."""
    classifier = SpamClassifier(models_dir="nonexistent/path")
    
    with pytest.raises(RuntimeError):
        classifier.load()


def test_classify_spam(classifier_mock):
    """Test classify method with spam email."""
    email_data = {"message": "Free money! Click here now!"}
    result = classifier_mock.classify(email_data)
    
    assert isinstance(result, dict)
    assert result["prediction"] == "spam"
    assert result["is_spam"] is True
    assert "confidence" in result
    assert "probability_spam" in result
    assert "probability_ham" in result
    assert "model_info" in result


def test_classify_ham(classifier_mock):
    """Test classify method with ham email."""
    # Mock to return ham
    classifier_mock.model.predict.return_value = [0]
    classifier_mock.model.predict_proba.return_value = [[0.90, 0.10]]
    
    email_data = {"message": "Hi, can we meet tomorrow?"}
    result = classifier_mock.classify(email_data)
    
    assert isinstance(result, dict)
    assert result["prediction"] == "ham"
    assert result["is_spam"] is False
    assert result["confidence"] > 0.5


def test_classify_not_loaded():
    """Test classify raises error when model is not loaded."""
    classifier = SpamClassifier(models_dir="tests/fixtures/models")
    
    with pytest.raises(RuntimeError):
        classifier.classify({"message": "Test email"})


def test_classify_confidence_calculation(classifier_mock):
    """Test confidence calculation in classify method."""
    # Set probabilities: [ham=0.1, spam=0.9]
    classifier_mock.model.predict_proba.return_value = [[0.1, 0.9]]
    
    email_data = {"message": "Test email"}
    result = classifier_mock.classify(email_data)
    
    # Confidence should be max(0.1, 0.9) = 0.9
    assert result["confidence"] == 0.9
    assert result["probability_spam"] == 0.9
    assert result["probability_ham"] == 0.1


def test_classify_model_info_included(classifier_mock):
    """Test that model_info is included in classification result."""
    email_data = {"message": "Test email"}
    result = classifier_mock.classify(email_data)
    
    assert "model_info" in result
    assert result["model_info"]["type"] == "LogisticRegression"
    assert result["model_info"]["vectorizer"] == "TfidfVectorizer"


def test_classify_empty_message(classifier_mock):
    """Test classify raises ValueError with empty message."""
    email_data = {"message": ""}
    with pytest.raises(ValueError):
        classifier_mock.classify(email_data)


def test_classify_linear_svc(classifier_mock):
    """Test classify with LinearSVC model (uses decision_function)."""
    from unittest.mock import MagicMock
    import numpy as np
    
    linear_svc_model = MagicMock()
    linear_svc_model.decision_function.return_value = np.array([2.5])
    linear_svc_model.__class__.__name__ = "LinearSVC"
    
    classifier_mock.model = linear_svc_model
    classifier_mock.metadata = {"model_type": "LinearSVC"}
    
    email_data = {"message": "Test email"}
    result = classifier_mock.classify(email_data)
    
    assert "prediction" in result
    assert "is_spam" in result
    assert "confidence" in result
    assert "probability_spam" in result
    assert "probability_ham" in result


def test_classify_fallback_path(classifier_mock):
    """Test classify fallback path for models without predict_proba."""
    from unittest.mock import MagicMock
    import numpy as np
    
    fallback_model = MagicMock()
    fallback_model.decision_function.return_value = np.array([1.5])
    fallback_model.__class__.__name__ = "UnknownModel"
    fallback_model.classes_ = ['ham', 'spam']
    
    classifier_mock.model = fallback_model
    
    email_data = {"message": "Test email"}
    result = classifier_mock.classify(email_data)
    
    assert "prediction" in result
    assert "is_spam" in result


def test_classify_with_threshold(classifier_mock):
    """Test classify with custom threshold."""
    classifier_mock.model.predict_proba.return_value = [[0.3, 0.7]]
    
    email_data = {"message": "Test email"}
    result = classifier_mock.classify(email_data, threshold=0.8)
    
    assert result["is_spam"] is False
    assert result["prediction"] == "ham"


def test_get_model_info_with_cv_metrics(classifier_mock):
    """Test get_model_info with CV metrics fallback."""
    classifier_mock.metadata = {
        "model_type": "LinearSVC",
        "cv_f1_mean": 0.95,
        "cv_f1_std": 0.02,
    }
    
    result = classifier_mock.get_model_info()
    assert result["f1_score"] == 0.95
    assert result["cv_f1_mean"] == 0.95
    assert result["cv_f1_std"] == 0.02


def test_load_with_label_encoder():
    """Test load includes label_encoder when available."""
    with patch("joblib.load") as mock_load:
        mock_model = MagicMock()
        mock_vectorizer = MagicMock()
        mock_label_encoder = MagicMock()
        mock_metadata = {}
        
        def load_side_effect(path):
            path_str = str(path)
            if "best_model_temp" in path_str:
                return mock_model
            elif "tfidf_vectorizer" in path_str:
                return mock_vectorizer
            elif "label_encoder" in path_str:
                return mock_label_encoder
            elif "metadata" in path_str:
                return mock_metadata
            return None
        
        mock_load.side_effect = load_side_effect
        
        # Mock Path.exists to return True for all files including label_encoder
        with patch.object(Path, "exists", autospec=True) as mock_exists:
            def exists_side_effect(path_instance):
                path_str = str(path_instance)
                # Return True for all required files
                if any([
                    "best_model_temp" in path_str,
                    "tfidf_vectorizer" in path_str,
                    "label_encoder" in path_str,
                    "metadata" in path_str
                ]):
                    return True
                return False
            mock_exists.side_effect = exists_side_effect
            
            classifier = SpamClassifier(models_dir="tests/fixtures/models")
            classifier.load()
        
        assert classifier.label_encoder == mock_label_encoder
        assert classifier.metadata == mock_metadata
        assert classifier.is_loaded is True

