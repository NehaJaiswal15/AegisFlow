from fastapi import FastAPI
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="AI-powered content moderation pipeline with multi-agent architecture",
    debug=settings.DEBUG,
)


@app.get("/healthz")
async def health_check():
    """Basic health check - returns OK if the server is running."""
    return {"status": "healthy", "project": settings.PROJECT_NAME}
