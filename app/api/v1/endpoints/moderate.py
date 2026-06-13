from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.moderation import ModerationRequest, ModerationResponse
from app.services.moderation_service import moderation_service
from app.core.database import get_db_session

router = APIRouter()


@router.post("/moderate", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Moderate text content for toxicity using the DistilBERT model."""
    result = await moderation_service.moderate(request.text, session)
    return ModerationResponse(**result)
