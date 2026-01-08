"""
Router for health check.
"""

from fastapi import APIRouter

from ..controllers import HealthController
from ..schemas import HealthResponse

router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check (Root)",
    description="Check if service is running and model is loaded",
)
@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if service is running and model is loaded",
)
async def health_check() -> HealthResponse:
    """Check service and model status."""
    from ..core import classifier

    health_data = HealthController.get_health_status(classifier)
    return HealthResponse(**health_data)

