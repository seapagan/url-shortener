"""Default configuration settings."""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Default BaseSettings."""

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortner.db"

    class Config:
        """Load env variables from .env file."""

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
