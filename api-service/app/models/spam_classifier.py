"""
Spam classification model for emails.

Loads and manages trained model to identify spam.
"""

from pathlib import Path
from typing import Any, Dict

import joblib


class SpamClassifier:
    """Spam classifier using trained model."""

    def __init__(self, models_dir: str = "models"):
        """Initialize the classifier.

        Args:
            models_dir: Path to directory with exported models
        """
        self.models_dir = Path(models_dir)
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.metadata = None
        self.is_loaded = False

    def load(self) -> None:
        """Load model and required artifacts."""
        try:
            model_path = self.models_dir / "best_model_temp.joblib"
            self.model = joblib.load(model_path)

            vectorizer_path = self.models_dir / "tfidf_vectorizer.joblib"
            self.vectorizer = joblib.load(vectorizer_path)

            # Load label_encoder if exists
            label_encoder_path = self.models_dir / "label_encoder.joblib"
            if label_encoder_path.exists():
                self.label_encoder = joblib.load(label_encoder_path)

            metadata_path = self.models_dir / "metadata.joblib"
            if metadata_path.exists():
                self.metadata = joblib.load(metadata_path)
            else:
                self.metadata = {}

            self.is_loaded = True

        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")

    def classify(self, data: Dict[str, Any], threshold: float = 0.5) -> Dict[str, Any]:
        """Classify email as spam or ham.

        Args:
            data: Dictionary with email data (field 'message')
            threshold: Probability threshold to classify as spam (default: 0.5)
                       Higher values (0.7-0.8) reduce false positives

        Returns:
            Dictionary with classification result
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Execute .load() first.")

        message = data.get("message", "")
        if not message:
            raise ValueError("Message cannot be empty")

        message_vectorized = self.vectorizer.transform([message])

        # Get probabilities from model (model must have predict_proba)
        if not hasattr(self.model, "predict_proba"):
            raise RuntimeError(
                "Model must have predict_proba method. Use CalibratedClassifierCV during training."
            )

        probabilities = self.model.predict_proba(message_vectorized)[0]
        classes = self.model.classes_

        spam_idx = list(classes).index("spam") if "spam" in classes else 1
        ham_idx = list(classes).index("ham") if "ham" in classes else 0

        probability_spam = float(probabilities[spam_idx])
        probability_ham = float(probabilities[ham_idx])

        is_spam = probability_spam >= threshold
        confidence = probability_spam if is_spam else probability_ham

        return {
            "prediction": "spam" if is_spam else "ham",
            "is_spam": is_spam,
            "confidence": round(confidence, 4),
            "probability_spam": round(probability_spam, 4),
            "probability_ham": round(probability_ham, 4),
            "model_info": {
                "type": self.metadata.get("base_model_type")
                or self.metadata.get("model_type", "Unknown"),
                "vectorizer": "TfidfVectorizer",
            },
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Return information about the loaded model."""
        if not self.is_loaded:
            return {"loaded": False}

        return {
            "loaded": True,
            "model_type": self.metadata.get("base_model_type")
            or self.metadata.get("model_type", "Unknown"),
            "vectorizer_type": "TfidfVectorizer",
            "training_samples": self.metadata.get("training_samples"),
            "accuracy": self.metadata.get("optimization_accuracy"),
            "precision": self.metadata.get("optimization_precision"),
            "recall": self.metadata.get("optimization_recall"),
            "f1_score": self.metadata.get("optimization_f1")
            or self.metadata.get("cv_f1_mean"),
            "trained_date": self.metadata.get("trained_date"),
            "cv_f1_mean": self.metadata.get("cv_f1_mean"),
            "cv_f1_std": self.metadata.get("cv_f1_std"),
        }

