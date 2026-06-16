from pydantic import BaseModel
from typing import Optional, Any


class TaskResponse(BaseModel):
    """Returned immediately when a task is queued."""
    task_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    """Returned when polling for task result."""
    task_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
