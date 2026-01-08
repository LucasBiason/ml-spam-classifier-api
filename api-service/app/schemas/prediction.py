"""
Prediction response schemas.
"""

from typing import List

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Classification response schema."""

    prediction: str = Field(..., description="Classification result: 'spam' or 'ham'")
    is_spam: bool = Field(..., description="Whether the email is spam")
    confidence: float = Field(
        ..., description="Prediction confidence score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    probability_spam: float = Field(
        ..., description="Probability of being spam", ge=0.0, le=1.0
    )
    probability_ham: float = Field(
        ..., description="Probability of being ham (not spam)", ge=0.0, le=1.0
    )
    model_info: dict = Field(..., description="Model information")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prediction": "spam",
                    "is_spam": True,
                    "confidence": 0.95,
                    "probability_spam": 0.95,
                    "probability_ham": 0.05,
                    "model_info": {
                        "type": "LogisticRegression",
                        "vectorizer": "TfidfVectorizer",
                    },
                },
                {
                    "prediction": "ham",
                    "is_spam": False,
                    "confidence": 0.88,
                    "probability_spam": 0.12,
                    "probability_ham": 0.88,
                    "model_info": {
                        "type": "LogisticRegression",
                        "vectorizer": "TfidfVectorizer",
                    },
                },
            ]
        }
    }

