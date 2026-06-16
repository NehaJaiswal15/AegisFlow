from fastapi import APIRouter
from celery.result import AsyncResult

from app.schemas.task import TaskResponse, TaskStatusResponse
from app.workers.celery_app import celery_app
from app.workers.tasks import moderate_text_task

router = APIRouter()


@router.post("/moderate/async", response_model=TaskResponse, status_code=202)
async def moderate_text_async(request: dict):
    """
    Queue a moderation task for background processing.
    Returns immediately with a task ID.
    """
    text = request.get("text", "")
    if not text or not text.strip():
        return TaskResponse(
            task_id="",
            status="FAILED",
            message="Text cannot be empty",
        )

    task = moderate_text_task.delay(text)

    return TaskResponse(
        task_id=task.id,
        status="QUEUED",
        message="Task has been queued for processing",
    )


@router.get("/tasks/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Poll for the result of a background moderation task."""
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return TaskStatusResponse(task_id=task_id, status="PENDING")
    elif result.state == "STARTED":
        return TaskStatusResponse(task_id=task_id, status="PROCESSING")
    elif result.state == "SUCCESS":
        return TaskStatusResponse(
            task_id=task_id,
            status="COMPLETED",
            result=result.result,
        )
    else:
        return TaskStatusResponse(
            task_id=task_id,
            status="FAILED",
            error=str(result.info),
        )
