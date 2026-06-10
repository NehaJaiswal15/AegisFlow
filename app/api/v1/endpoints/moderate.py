from fastapi import APIRouter

from app.schemas.moderation import ModerationRequest, ModerationResponse
from app.services.moderation_service import moderation_service

router = APIRouter()


@router.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: ModerationRequest):
    """Moderate text content for toxicity using the DistilBERT model."""
    result = moderation_service.moderate(request.text)
    return ModerationResponse(**result)
