import time
from uuid import uuid4
from datetime import datetime, timezone

from app.repositories.model_repository import model_repo


class ModerationService:
    """
    Business logic for content moderation.
    Calls the model repository and interprets the result.
    """

    def moderate(self, text: str) -> dict:
        """Run the full moderation pipeline on the given text."""
        start_time = time.time()

        # Call Agent 1: Your DistilBERT model
        prediction = model_repo.predict(text)

        # Interpret the result
        score = prediction["score"]
        label = prediction["label"]

        # The model returns "toxic" or "non-toxic" as labels
        # If label is "non-toxic", flip the score
        if label.lower() in ["non-toxic", "non_toxic", "not toxic", "neutral"]:
            toxicity_score = 1.0 - score
        else:
            toxicity_score = score

        # Decide the verdict based on score thresholds
        if toxicity_score >= 0.7:
            verdict = "TOXIC"
        elif toxicity_score >= 0.4:
            verdict = "NEEDS_REVIEW"
        else:
            verdict = "SAFE"

        processing_time = (time.time() - start_time) * 1000

        return {
            "moderation_id": uuid4(),
            "verdict": verdict,
            "toxicity_score": round(toxicity_score, 4),
            "model_version": prediction["model_version"],
            "processing_time_ms": round(processing_time, 2),
            "timestamp": datetime.now(timezone.utc),
        }


# Single global instance
moderation_service = ModerationService()
