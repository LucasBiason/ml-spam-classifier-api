"""
Controller for spam prediction operations.
"""

from typing import Any, Dict

from fastapi import HTTPException, status


class PredictionController:
    """Controller for spam classification."""

    @staticmethod
    def get_model_info(classifier) -> Dict[str, Any]:
        """Return model information."""
        return classifier.get_model_info()

    @staticmethod
    def classify_email(classifier, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify email as spam or ham.

        Args:
            classifier: Classifier instance
            email_data: Email data (message and optionally threshold)

        Raises:
            HTTPException: If model is not loaded or an error occurs
        """
        if not classifier.is_loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded. Please try again in a few seconds.",
            )

        try:
            threshold = email_data.get("threshold", 0.5)
            return classifier.classify(email_data, threshold=threshold)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Classification error: {str(e)}",
            )

