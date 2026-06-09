from fastapi import APIRouter
from app.api.v1.endpoints import moderate

api_router = APIRouter()

api_router.include_router(moderate.router, tags=["Moderation"])
