import time
from uuid import uuid4
from datetime import datetime, timezone

from app.workers.celery_app import celery_app
from app.repositories.model_repository import model_repo


@celery_app.task(
    name="moderate_text",
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def moderate_text_task(self, text: str) -> dict:
    """
    Background task that runs the moderation pipeline.
    Retries up to 3 times with 5-second delay if something goes wrong.
    """
    try:
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

        return {
            "moderation_id": str(uuid4()),
            "verdict": verdict,
            "toxicity_score": round(toxicity_score, 4),
            "model_version": prediction["model_version"],
            "processing_time_ms": round(processing_time, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        print(f"Task failed (attempt {self.request.retries + 1}/3): {exc}")
        raise self.retry(exc=exc)
