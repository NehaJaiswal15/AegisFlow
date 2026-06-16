from fastapi import APIRouter
from app.api.v1.endpoints import moderate, feedback, tasks

api_router = APIRouter()

api_router.include_router(moderate.router, tags=["Moderation"])
api_router.include_router(feedback.router, tags=["Feedback"])
api_router.include_router(tasks.router, tags=["Tasks"])
