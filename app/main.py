from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import api_router
from app.repositories.model_repository import model_repo


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup and shutdown."""
    # STARTUP: Load the ML model into memory
    model_repo.load_model(settings.MODEL_NAME)
    yield
    # SHUTDOWN: Cleanup (nothing to do for now)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="AI-powered content moderation pipeline with multi-agent architecture",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/healthz")
async def health_check():
    """Basic health check - returns OK if the server is running."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "model_loaded": model_repo.is_loaded(),
    }
