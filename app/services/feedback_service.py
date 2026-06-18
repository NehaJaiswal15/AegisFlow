from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.feedback_db_repository import feedback_db_repo
from app.core.exceptions import ModerationNotFoundError


class FeedbackService:
    """Business logic for processing feedback."""

    async def process_feedback(
        self, moderation_id, correct_verdict, feedback_source, session: AsyncSession
    ) -> dict:
        """Compare human feedback with model's original prediction."""

        original = await feedback_db_repo.get_moderation_by_id(session, moderation_id)

        if original is None:
            raise ModerationNotFoundError(str(moderation_id))

        was_correct = original.verdict == correct_verdict

        feedback_data = {
            "feedback_id": uuid4(),
            "moderation_id": moderation_id,
            "correct_verdict": correct_verdict,
            "feedback_source": feedback_source,
            "was_model_correct": was_correct,
            "recorded_at": datetime.now(timezone.utc),
        }

        await feedback_db_repo.save(session, feedback_data)

        return feedback_data


feedback_service = FeedbackService()
