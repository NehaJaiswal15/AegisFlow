from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional



class ModerationRequest(BaseModel):
    """What the client sends us."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to be moderated"
    )
    language: str = Field(
        default="en",
        description="Language code (e.g., 'en')"
    )
    
class ModerationResponse(BaseModel):
    """What we send back."""
    moderation_id: UUID
    verdict: str
    toxicity_score: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    processing_time_ms: float
    timestamp: datetime
    from_cache: bool = False


    model_config = {"protected_namespaces": ()}