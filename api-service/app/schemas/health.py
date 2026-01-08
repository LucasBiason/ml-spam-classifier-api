"""
Health check response schema.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(..., description="Service status")
    timestamp: Optional[datetime] = Field(None, description="Check timestamp")
    model_loaded: Optional[bool] = Field(None, description="Whether model is loaded")
    version: Optional[str] = Field(None, description="API version")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "timestamp": "2025-01-06T10:30:00",
                    "model_loaded": True,
                    "version": "1.0.0",
                }
            ]
        }
    }

