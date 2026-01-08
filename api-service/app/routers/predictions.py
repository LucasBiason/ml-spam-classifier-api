"""
Router for prediction endpoints.
"""

from fastapi import APIRouter

from ..controllers import PredictionController
from ..schemas import EmailInput, ErrorResponse, ModelInfoResponse, PredictionResponse

router = APIRouter()


@router.get(
    "/model/info",
    response_model=ModelInfoResponse,
    summary="Model Information",
    description="Get detailed information about the loaded model",
)
async def model_info() -> ModelInfoResponse:
    """Model information endpoint."""
    from ..core import classifier

    info = PredictionController.get_model_info(classifier)
    return ModelInfoResponse(**info)


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Classify Email",
    description="Classify email as spam or ham using trained model",
    responses={
        200: {"description": "Classification successful"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def classify_email(email_data: EmailInput) -> PredictionResponse:
    """Main email classification endpoint."""
    from ..core import classifier

    data = email_data.model_dump()
    result = PredictionController.classify_email(classifier, data)
    return PredictionResponse(**result)

