import time
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.moderation import ModerationRequest, ModerationResponse

router = APIRouter()


@router.post("/moderate", response_model=ModerationResponse)
async def moderate_text(request: ModerationRequest):
    """
    Moderate text content for toxicity.
    For now, returns a dummy response. We'll plug in the real ML model next.
    """
    start_time = time.time()

    # TODO: Replace this with real model prediction in Step 1.4
    dummy_score = 0.15
    verdict = "TOXIC" if dummy_score > 0.5 else "SAFE"

    processing_time = (time.time() - start_time) * 1000  # Convert to ms

    return ModerationResponse(
        moderation_id=uuid4(),
        verdict=verdict,
        toxicity_score=dummy_score,
        model_version="dummy-v0",
        processing_time_ms=round(processing_time, 2),
        timestamp=datetime.now(timezone.utc),
    )
