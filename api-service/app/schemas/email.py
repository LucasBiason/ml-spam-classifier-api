"""
Input schema for spam classification.
"""

from pydantic import BaseModel, Field, field_validator


class EmailInput(BaseModel):
    """Input schema for classification."""

    message: str = Field(
        ...,
        description="Email message text to classify",
        min_length=10,
        max_length=5000,
    )
    threshold: float = Field(
        default=0.5,
        description=(
            "Probability threshold to classify as spam (0.0-1.0). "
            "Higher values (0.7-0.8) reduce false positives"
        ),
        ge=0.0,
        le=1.0,
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate and normalize message."""
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Free money! Click here now to claim your prize! Limited time offer!!!",
                },
                {
                    "message": "Hi, I wanted to follow up on our meeting from yesterday. Can we schedule a call this week?",
                },
            ]
        }
    }

