import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, Boolean, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app.core.database import Base


class ModerationLog(Base):
    """Every moderation decision is saved here — your audit trail."""
    __tablename__ = "moderation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_text = Column(Text, nullable=False)
    text_hash = Column(String(64), index=True)
    verdict = Column(String(20), nullable=False)
    toxicity_score = Column(Float, nullable=False)
    model_version = Column(String(20))
    escalated = Column(Boolean, default=False)
    processing_time_ms = Column(Float)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    def __repr__(self):
        return f"<ModerationLog {self.id} verdict={self.verdict} score={self.toxicity_score}>"
