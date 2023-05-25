import pytest

# noinspection PyUnresolvedReferences
from app.tests.fixtures import memory_movie_repo_fixture
from app.entities.movie import Movie
from app.repository.movie.abstractions import RepositoryException


@pytest.mark.asyncio
async def test_create(memory_movie_repo_fixture):
    test_movie = Movie(
        movie_id="test",
        title="test movie",
        description="test description",
        release_year=1999,
    )
    await memory_movie_repo_fixture.create(test_movie)
    assert await memory_movie_repo_fixture.get_by_id("test") is test_movie


@pytest.mark.parametrize(
    "movies_seed,movie_id,expected_result",
    [
        pytest.param([], "my_id", None, id="No movie"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                )
            ],
            "my-id",
            Movie(
                movie_id="my-id",
                title="test movie",
                description="test description",
                release_year=1999,
            ),
            id="Valid movie",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    memory_movie_repo_fixture, movies_seed, movie_id, expected_result
):
    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    # noinspection PyTypeChecker
    movie = await memory_movie_repo_fixture.get_by_id(movie_id=movie_id)
    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed,movie_title,expected_result",
    [
        pytest.param([], "some_title", [], id="No movie"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                )
            ],
            "some_title",
            [],
            id="movie sent but another expected",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                )
            ],
            "test_title",
            [
                Movie(
                    movie_id="my-id",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                )
            ],
            id="Valid movie",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="my-id4",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="my-id5",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            [
                Movie(
                    movie_id="my-id4",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="my-id5",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            id="2 movies",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(
    memory_movie_repo_fixture, movies_seed, movie_title, expected_result
):
    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    # noinspection PyTypeChecker
    movie = await memory_movie_repo_fixture.get_by_title(title=movie_title)
    assert movie == expected_result


# noinspection DuplicatedCode
@pytest.mark.parametrize(
    "movies_seed, movie_title, skip, limit, expected_result",
    [
        pytest.param(
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            0,
            0,
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            id="Skip 0, Limit 0",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            0,
            1,
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                )
            ],
            id="Skip 0, Limit 1",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "test_title",
            1,
            1,
            [
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                )
            ],
            id="Skip 1, Limit 1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title_pagination(
    memory_movie_repo_fixture, movies_seed, movie_title, skip, limit, expected_result
):
    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    movie = await memory_movie_repo_fixture.get_by_title(
        title=movie_title, skip=skip, limit=limit
    )
    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed, skip, limit, expected_result",
    [
        pytest.param(
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            0,
            0,
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            id="Skip 0, Limit 0",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            0,
            1,
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                )
            ],
            id="Skip 0, Limit 1",
        ),
        pytest.param(
            [
                Movie(
                    movie_id="someid1",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    movie_id="someid3",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                ),
            ],
            1,
            1,
            [
                Movie(
                    movie_id="someid2",
                    title="test_title",
                    description="test description",
                    release_year=1999,
                )
            ],
            id="Skip 1, Limit 1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_all(
    memory_movie_repo_fixture, movies_seed, skip, limit, expected_result
):
    for movie in movies_seed:
        await memory_movie_repo_fixture.create(movie)
    movies = await memory_movie_repo_fixture.get_all(skip=skip, limit=limit)
    assert movies == expected_result


@pytest.mark.asyncio
async def test_update(memory_movie_repo_fixture):
    await memory_movie_repo_fixture.create(
        Movie(
            movie_id="my-id9",
            title="test_title",
            description="test description",
            release_year=1999,
            watched=False,
        )
    )
    await memory_movie_repo_fixture.update(
        movie_id="my-id9",
        update_parameters={
            "title": "updated title",
            "description": "updated description",
            "release_year": 2000,
            "watched": True,
        },
    )
    movie = await memory_movie_repo_fixture.get_by_id("my-id9")
    assert movie == Movie(
        movie_id="my-id9",
        title="updated title",
        description="updated description",
        release_year=2000,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_negative(memory_movie_repo_fixture):
    await memory_movie_repo_fixture.create(
        Movie(
            movie_id="my-id8",
            title="test_title",
            description="test description",
            release_year=1999,
        )
    )

    with pytest.raises(RepositoryException):
        await memory_movie_repo_fixture.update(
            movie_id="my_id8", update_parameters={"id": "trying to change the ID"}
        )


@pytest.mark.asyncio
async def test_delete(memory_movie_repo_fixture):
    await memory_movie_repo_fixture.create(
        Movie(
            movie_id="my-id6",
            title="test_title",
            description="test description",
            release_year=1999,
        )
    )

    await memory_movie_repo_fixture.delete("my_id6")
    assert await memory_movie_repo_fixture.get_by_id("my_id6") is None
