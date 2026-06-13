from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Literal


class FeedbackRequest(BaseModel):
    """What the reviewer sends."""
    moderation_id: UUID
    correct_verdict: Literal["SAFE", "TOXIC", "NEEDS_REVIEW"]
    feedback_source: str = Field(
        default="human_reviewer",
        description="Who provided the feedback"
    )


class FeedbackResponse(BaseModel):
    """What we send back."""
    feedback_id: UUID
    moderation_id: UUID
    was_model_correct: bool
    recorded_at: datetime

    model_config = {"protected_namespaces": ()}
