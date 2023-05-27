import asyncio
import secrets

import pytest
from starlette.testclient import TestClient

from app.api import create_app
from app.repository.movie.memory import MemoryMovieRepository
from app.repository.movie.mongo import MongoMovieRepository

# noinspection PyPackageRequirements


@pytest.fixture()
def mongo_movie_repo_fixture():
    random_database_name = secrets.token_hex(5)
    repo = MongoMovieRepository(
        connection_string="mongodb://localhost:27017", database=random_database_name
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
