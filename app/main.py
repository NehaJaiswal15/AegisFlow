from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.repositories.model_repository import model_repo

# Import models so SQLAlchemy knows about them
from app.models.database import ModerationLog  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup and shutdown."""
    # STARTUP: Create database tables + load ML model
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

    model_repo.load_model(settings.MODEL_NAME)
    yield
    # SHUTDOWN: Close database connections
    await engine.dispose()


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
