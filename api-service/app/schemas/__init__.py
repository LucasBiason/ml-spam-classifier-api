"""
Pydantic schemas for API validation.
"""

from .email import EmailInput
from .error import ErrorResponse
from .health import HealthResponse
from .model_info import ModelInfoResponse
from .prediction import PredictionResponse

__all__ = [
    "EmailInput",
    "PredictionResponse",
    "HealthResponse",
    "ModelInfoResponse",
    "ErrorResponse",
]

