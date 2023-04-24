import secrets

import pytest

# noinspection PyUnresolvedReferences
from api._tests.fixtures import mongo_movie_repo_fixture
from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException


@pytest.mark.asyncio
async def test_create(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        movie=Movie(
            movie_id="test first",
            title="some title",
            description="some desc",
            release_year=1995,
            watched=False,
        )
    )
    movie: Movie = await mongo_movie_repo_fixture.get_by_id("test first")
    assert movie == Movie(
        movie_id="test first",
        title="some title",
        description="some desc",
        release_year=1995,
        watched=False,
    )


@pytest.mark.parametrize(
    "input_movies, movie_id, expected_result",
    [
        pytest.param([], "any", None, id="empty input"),
        pytest.param(
            [
                Movie(
                    movie_id="test first",
                    title="some title",
                    description="some desc",
                    release_year=1995,
                    watched=False,
                ),
                Movie(
                    movie_id="second",
                    title="second title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
            ],
            "second",
            Movie(
                movie_id="second",
                title="second title",
                description="second desc",
                release_year=1992,
                watched=True,
            ),
            id="valid movie",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    mongo_movie_repo_fixture, input_movies, movie_id, expected_result
):
    for movie in input_movies:
        await mongo_movie_repo_fixture.create(movie)
    movie: Movie = await mongo_movie_repo_fixture.get_by_id(movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "input_movies, searched_title, expected_result",
    [
        pytest.param([], "non existent movie", [], id="no input"),
        pytest.param(
            [
                Movie(
                    movie_id="test title2",
                    title="same title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
                Movie(
                    movie_id="test title3",
                    title="same title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
            ],
            "same title",
            [
                Movie(
                    movie_id="test title2",
                    title="same title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
                Movie(
                    movie_id="test title3",
                    title="same title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
            ],
            id="two inputs with the same title",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(
    mongo_movie_repo_fixture, input_movies, searched_title, expected_result
):
    for movie in input_movies:
        await mongo_movie_repo_fixture.create(movie)
    movie: Movie = await mongo_movie_repo_fixture.get_by_title(title=searched_title)
    assert movie == expected_result


@pytest.mark.asyncio
async def test_update(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="some id",
            title="some title",
            description="second desc",
            release_year=1992,
            watched=False,
        )
    )
    await mongo_movie_repo_fixture.update(
        movie_id="some id",
        update_parameters={
            "title": "updated title",
            "description": "updated description",
            "release_year": 2000,
            "watched": True,
        },
    )
    assert await mongo_movie_repo_fixture.get_by_id("some id") == Movie(
        movie_id="some id",
        title="updated title",
        description="updated description",
        release_year=2000,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_negative(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="test title3",
            title="same title",
            description="second desc",
            release_year=1992,
            watched=True,
        )
    )
    with pytest.raises(RepositoryException):
        await mongo_movie_repo_fixture.update(
            movie_id="test title3", update_parameters={"id": "updated id"}
        )


@pytest.mark.asyncio
async def test_delete(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            movie_id="test title3",
            title="same title",
            description="second desc",
            release_year=1992,
            watched=True,
        )
    )
    assert await mongo_movie_repo_fixture.delete("test title3") is None

@pytest.mark.asyncio
async def test_delete_not_found(mongo_movie_repo_fixture):
    with pytest.raises(RepositoryException):
        assert await mongo_movie_repo_fixture.delete(secrets.token_hex(10))


