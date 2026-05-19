from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://redis:6379"
    MAX_REQUESTS: int = 10        # requests per window
    WINDOW_SECONDS: int = 60      # window size in seconds

    class Config:
        env_file = ".env"

settings = Settings()