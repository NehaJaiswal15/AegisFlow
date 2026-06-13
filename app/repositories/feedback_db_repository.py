from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import FeedbackLog, ModerationLog


class FeedbackDBRepository:
    """Handles database operations for feedback."""

    async def save(self, session: AsyncSession, feedback_data: dict) -> FeedbackLog:
        """Save feedback to the database."""
        log = FeedbackLog(
            id=feedback_data["feedback_id"],
            moderation_id=feedback_data["moderation_id"],
            correct_verdict=feedback_data["correct_verdict"],
            feedback_source=feedback_data["feedback_source"],
            was_model_correct=feedback_data["was_model_correct"],
        )
        session.add(log)
        await session.flush()
        return log

    async def get_moderation_by_id(self, session: AsyncSession, moderation_id: UUID) -> ModerationLog | None:
        """Look up the original moderation decision."""
        result = await session.execute(
            select(ModerationLog).where(ModerationLog.id == moderation_id)
        )
        return result.scalar_one_or_none()


feedback_db_repo = FeedbackDBRepository()
