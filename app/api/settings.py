from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # MongoDB Settings
    mongo_connection_string: str = Field(
        "mongodb://localhost:27017",
        title="MongoDB connection string",
        description="MongoDB database connection string.",
        env="MONGODB_CONNECTION_STRING",
    )
    mongo_database_name: str = Field(
        "movie_track_db",
        title="MongoDB Movies Database Name",
        description="MongoDB Movies Database Name",
        env="MONGODB_DATABASE_NAME",
    )


@lru_cache()
def settings_instance():
    """
    Settings instance to be used as a FastAPI dependency.
    """
    return Settings()
