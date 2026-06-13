import hashlib
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import ModerationLog


class ModerationDBRepository:
    """Handles all database operations for moderation logs."""

    @staticmethod
    def _hash_text(text: str) -> str:
        """Create a SHA256 hash of the input text."""
        return hashlib.sha256(text.encode()).hexdigest()

    async def save(self, session: AsyncSession, moderation_data: dict, input_text: str) -> ModerationLog:
        """Save a moderation result to the database."""
        log = ModerationLog(
            id=moderation_data["moderation_id"],
            input_text=input_text,
            text_hash=self._hash_text(input_text),
            verdict=moderation_data["verdict"],
            toxicity_score=moderation_data["toxicity_score"],
            model_version=moderation_data["model_version"],
            processing_time_ms=moderation_data["processing_time_ms"],
        )
        session.add(log)
        await session.flush()  # Sends INSERT to DB without committing yet
        return log

    async def get_by_id(self, session: AsyncSession, moderation_id: UUID) -> ModerationLog | None:
        """Look up a specific moderation decision."""
        result = await session.execute(
            select(ModerationLog).where(ModerationLog.id == moderation_id)
        )
        return result.scalar_one_or_none()

    async def get_recent(self, session: AsyncSession, limit: int = 20) -> list[ModerationLog]:
        """Get the most recent moderation decisions."""
        result = await session.execute(
            select(ModerationLog).order_by(ModerationLog.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())


# Single global instance
moderation_db_repo = ModerationDBRepository()
