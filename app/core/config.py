from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    Reads values from the .env file automatically.
    """

    PROJECT_NAME: str = "AegisFlow"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    MODEL_NAME: str = "martin-ha/toxic-comment-model"

    # Database settings
    DB_USER: str = "aegisflow"
    DB_PASSWORD: str = "aegisflow_secret"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_NAME: str = "content_moderation"

    # Redis & Celery settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    @property
    def DATABASE_URL(self) -> str:
        """Build the async database connection string."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


# Create a single instance that the whole app will use
settings = Settings()

