from celery import Celery
from celery.signals import worker_process_init
from app.core.config import settings

celery_app = Celery(
    "aegisflow",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"],
)


celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    task_track_started=True,
    result_expires=3600,
)


@worker_process_init.connect
def load_model_on_worker_start(**kwargs):
    """Load the ML model when the Celery worker process starts."""
    from app.repositories.model_repository import model_repo
    if not model_repo.is_loaded():
        model_repo.load_model(settings.MODEL_NAME)
