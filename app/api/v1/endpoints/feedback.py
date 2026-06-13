from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.services.feedback_service import feedback_service
from app.core.database import get_db_session

router = APIRouter()


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Submit human feedback on a moderation decision."""
    try:
        result = await feedback_service.process_feedback(
            moderation_id=request.moderation_id,
            correct_verdict=request.correct_verdict,
            feedback_source=request.feedback_source,
            session=session,
        )
        return FeedbackResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
