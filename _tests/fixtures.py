import asyncio
import secrets

import pytest
from starlette.testclient import TestClient

from app.api.api import create_app
from app.api.repository.movie.memory import MemoryMovieRepository
from app.api.repository.movie.mongo import MongoMovieRepository


@pytest.fixture()
def test_client():
    client = TestClient(app=create_app())
    client.headers = {"Authorization": "Basic YWRtaW46YWRtaW4="}

    return client


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
