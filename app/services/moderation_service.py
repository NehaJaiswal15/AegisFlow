import time
from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.model_repository import model_repo
from app.repositories.moderation_db_repository import moderation_db_repo
from app.repositories.cache_repository import cache_repo


class ModerationService:
    """
    Business logic for content moderation.
    Checks cache first, then runs the model if needed.
    """

    async def moderate(self, text: str, session: AsyncSession) -> dict:
        """Run the full moderation pipeline on the given text."""

        # Step 1: Check the cache
        cached_result = cache_repo.get(text)
        if cached_result:
            cached_result["moderation_id"] = str(uuid4())
            cached_result["timestamp"] = datetime.now(timezone.utc).isoformat()
            cached_result["from_cache"] = True
            return cached_result

        # Step 2: Cache miss — run the model
        start_time = time.time()

        prediction = model_repo.predict(text)

        score = prediction["score"]
        label = prediction["label"]

        if label.lower() in ["non-toxic", "non_toxic", "not toxic", "neutral"]:
            toxicity_score = 1.0 - score
        else:
            toxicity_score = score

        if toxicity_score >= 0.7:
            verdict = "TOXIC"
        elif toxicity_score >= 0.4:
            verdict = "NEEDS_REVIEW"
        else:
            verdict = "SAFE"

        processing_time = (time.time() - start_time) * 1000

        result = {
            "moderation_id": str(uuid4()),
            "verdict": verdict,
            "toxicity_score": round(toxicity_score, 4),
            "model_version": prediction["model_version"],
            "processing_time_ms": round(processing_time, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_cache": False,
        }

        # Step 3: Save to cache for next time
        cache_repo.save(text, {
            "verdict": verdict,
            "toxicity_score": round(toxicity_score, 4),
            "model_version": prediction["model_version"],
            "processing_time_ms": 0.0,
        })

        # Step 4: Save to database
        db_data = {
            **result,
            "moderation_id": uuid4(),
            "timestamp": datetime.now(timezone.utc),
        }
        await moderation_db_repo.save(session, db_data, text)

        return result


moderation_service = ModerationService()
