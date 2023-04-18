import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.memory import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MemoryMovieRepository()
    test_movie = Movie(
        movie_id="test",
        title="test movie",
        description="test description",
        release_year=1999,
    )
    await repo.create(test_movie)
    assert await repo.get_by_id("test") is test_movie


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
async def test_get_by_id(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    # noinspection PyTypeChecker
    movie = await repo.get_by_id(movie_id=movie_id)
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
async def test_get_by_title(movies_seed, movie_title, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)
    # noinspection PyTypeChecker
    movie = await repo.get_by_title(title=movie_title)
    assert movie == expected_result


@pytest.mark.asyncio
async def test_update():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id9",
            title="test_title",
            description="test description",
            release_year=1999,
            watched=False,
        )
    )
    await repo.update(
        movie_id="my-id9",
        update_parameters={
            "title": "updated title",
            "description": "updated description",
            "release_year": 2000,
            "watched": True,
        },
    )
    movie = await repo.get_by_id("my-id9")
    assert movie == Movie(
        movie_id="my-id9",
        title="updated title",
        description="updated description",
        release_year=2000,
        watched=True,
    )


@pytest.mark.asyncio
async def test_update_negative():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id8",
            title="test_title",
            description="test description",
            release_year=1999,
        )
    )

    with pytest.raises(RepositoryException):
        await repo.update(
            movie_id="my_id8", update_parameters={"id": "trying to change the ID"}
        )


@pytest.mark.asyncio
async def test_delete():
    repo = MemoryMovieRepository()
    await repo.create(
        Movie(
            movie_id="my-id6",
            title="test_title",
            description="test description",
            release_year=1999,
        )
    )

    await repo.delete("my_id6")
    assert await repo.get_by_id("my_id6") is None
