from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str
    mongo_database_name: str

    class Config:
        env_file = "settings.env"


@lru_cache()
def settings_instance():
    """Settings instance to be used as a FastAPI dependency."""

    return Settings()
