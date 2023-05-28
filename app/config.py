from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str
    mongo_database_name: str
    server_selection_timeout_ms: float

    class Config:
        env_file = "settings.env"


class TestSettings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str
    # mongo_database_name: str
    server_selection_timeout_ms: float

    class Config:
        env_file = "test_settings.env"


@lru_cache()
def settings_instance():
    """Settings instance to be used as a FastAPI dependency."""

    return Settings()


@lru_cache()
def test_settings_instance():
    """Settings instance to be used as a FastAPI dependency for tests."""

    return TestSettings()
