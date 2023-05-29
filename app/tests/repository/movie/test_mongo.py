import secrets
from typing import List

import pytest

from app.entities.movie import Movie
from app.repository.movie.abstractions import RepositoryException

# noinspection PyUnresolvedReferences
from app.tests.fixtures import mongo_movie_repo_fixture


@pytest.mark.asyncio
async def test_create(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        movie=Movie(
            id="test first",
            title="some title",
            description="some desc",
            release_year=1995,
            watched=False,
        )
    )
    movie: Movie = await mongo_movie_repo_fixture.get_by_id("test first")
    assert movie == Movie(
        id="test first",
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
                    id="test first",
                    title="some title",
                    description="some desc",
                    release_year=1995,
                    watched=False,
                ),
                Movie(
                    id="second",
                    title="second title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
            ],
            "second",
            Movie(
                id="second",
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
        pytest.param([], "non existent movie", ([], 0), id="no input"),
        pytest.param(
            [
                Movie(
                    id="test title2",
                    title="same title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
                Movie(
                    id="test title3",
                    title="same title",
                    description="second desc",
                    release_year=1992,
                    watched=True,
                ),
            ],
            "same title",
            (
                [
                    Movie(
                        id="test title2",
                        title="same title",
                        description="second desc",
                        release_year=1992,
                        watched=True,
                    ),
                    Movie(
                        id="test title3",
                        title="same title",
                        description="second desc",
                        release_year=1992,
                        watched=True,
                    ),
                ],
                2,
            ),
            id="two inputs with the same title",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_fields(
    mongo_movie_repo_fixture, input_movies, searched_title, expected_result
):
    for movie in input_movies:
        await mongo_movie_repo_fixture.create(movie)
    response: tuple[list[Movie], int] = await mongo_movie_repo_fixture.get_by_fields(
        title=searched_title
    )
    assert response == expected_result


# noinspection DuplicatedCode
@pytest.mark.parametrize(
    "movies_seed, movie_title, skip, limit, expected_result",
    [
        pytest.param(
            [
                Movie(
                    id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            0,
            0,
            (
                [
                    Movie(
                        id="someid1",
                        title="test_title",
                        description="test description",
                        release_year=1999,
                    ),
                    Movie(
                        id="someid2",
                        title="test_title",
                        description="test description",
                        release_year=1999,
                    ),
                    Movie(
                        id="someid3",
                        title="test_title",
                        description="test description",
                        release_year=1999,
                    ),
                ],
                3,
            ),
            id="Skip 0, Limit 0",
        ),
        pytest.param(
            [
                Movie(
                    id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            0,
            1,
            (
                [
                    Movie(
                        id="someid1",
                        title="test_title",
                        description="test description",
                        release_year=1999,
                    )
                ],
                3,
            ),
            id="Skip 0, Limit 1",
        ),
        pytest.param(
            [
                Movie(
                    id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            1,
            1,
            (
                [
                    Movie(
                        id="someid2",
                        title="test_title",
                        description="test description",
                        release_year=1999,
                    )
                ],
                3,
            ),
            id="Skip 1, Limit 1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title_pagination(
    mongo_movie_repo_fixture, movies_seed, movie_title, skip, limit, expected_result
):
    for movie in movies_seed:
        await mongo_movie_repo_fixture.create(movie)
    response = await mongo_movie_repo_fixture.get_by_fields(
        title=movie_title, skip=skip, limit=limit
    )
    assert response == expected_result


@pytest.mark.asyncio
async def test_update(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            id="some id",
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
        id="some id",
        title="updated title",
        description="updated description",
        release_year=2000,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_negative(mongo_movie_repo_fixture):
    await mongo_movie_repo_fixture.create(
        Movie(
            id="test title3",
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
            id="test title3",
            title="same title",
            description="second desc",
            release_year=1992,
            watched=True,
        )
    )
    assert await mongo_movie_repo_fixture.delete("test title3") is None
    read_result = await mongo_movie_repo_fixture.get_by_id(movie_id="test title3")
    assert read_result is None


@pytest.mark.asyncio
async def test_delete_not_found(mongo_movie_repo_fixture):
    assert await mongo_movie_repo_fixture.delete(secrets.token_hex(10)) is None
