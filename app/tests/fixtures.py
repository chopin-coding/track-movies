import asyncio
import secrets

import pytest
from starlette.testclient import TestClient

from app.api import create_app
from app.config import TestSettings, test_settings_instance
from app.repository.movie.memory import MemoryMovieRepository
from app.repository.movie.mongo import MongoMovieRepository

# noinspection PyPackageRequirements


@pytest.fixture()
def mongo_movie_repo_fixture(
    settings: TestSettings = lambda: test_settings_instance(),
) -> MongoMovieRepository:
    random_database_name = secrets.token_hex(5)
    repo = MongoMovieRepository(
        connection_string=settings().mongo_connection_string,
        database=random_database_name,
        server_selection_timeout_ms=settings().server_selection_timeout_ms,
    )
    yield repo

    loop = asyncio.get_event_loop()
    # noinspection PyProtectedMember
    loop.run_until_complete(repo._client.drop_database(random_database_name))


@pytest.fixture()
def memory_movie_repo_fixture():
    repo = MemoryMovieRepository()
    yield repo
    del repo


@pytest.fixture()
def test_client():
    return TestClient(app=create_app())
