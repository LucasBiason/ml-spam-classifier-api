"""
Model information schema.
"""

from typing import Optional

from pydantic import BaseModel, Field


class ModelInfoResponse(BaseModel):
    """Detailed model information schema."""

    loaded: bool = Field(..., description="Whether model is loaded")
    model_type: Optional[str] = Field(None, description="Model type")
    vectorizer_type: Optional[str] = Field(None, description="Vectorizer type")
    training_samples: Optional[int] = Field(None, description="Training samples count")
    accuracy: Optional[float] = Field(None, description="Model accuracy")
    precision: Optional[float] = Field(None, description="Model precision")
    recall: Optional[float] = Field(None, description="Model recall")
    f1_score: Optional[float] = Field(None, description="Model F1 score")
    trained_date: Optional[str] = Field(None, description="Training date")





