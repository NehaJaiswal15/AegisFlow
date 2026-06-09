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

    class Config:
        env_file = ".env"


# Create a single instance that the whole app will use
settings = Settings()
