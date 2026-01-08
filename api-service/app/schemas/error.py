"""
Error response schema.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Error type")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Error timestamp"
    )

