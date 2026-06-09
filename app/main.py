from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router



app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="AI-powered content moderation pipeline with multi-agent architecture",
    debug=settings.DEBUG,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/healthz")
async def health_check():
    """Basic health check - returns OK if the server is running."""
    return {"status": "healthy", "project": settings.PROJECT_NAME}
