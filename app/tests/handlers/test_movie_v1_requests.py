import pytest

from app.entities.movie import Movie
# noinspection PyUnresolvedReferences
from app.tests.fixtures import test_client


# FIXME: Pytest can't read env variables even
#  after pytest-dotenv

# FIXME: Adapt all of the test to only use test_client requests
#  and no repos directly

@pytest.mark.asyncio()
async def test_create_movie(test_client):
    # Test
    create_result = test_client.post(
        "/api/v1/movie/",
        json={
            "title": "some",
            "description": "string",
            "release_year": 2004,
            "watched": False,
        },
    )

    # Assert
    movie_id = create_result.json().get("id")
    assert create_result.status_code == 201

    get_result = test_client.get(f"/api/v1/movie/{movie_id}")
    assert get_result.status_code == 200
    assert get_result is not None


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movie_json",
    [
        (
            {
                "description": "string",
                "release_year": 2004,
                "watched": False,
            },
        ),
        (
            {
                "title": "My Movie1",
                "release_year": 2004,
                "watched": False,
            },
        ),
        (
            {
                "title": "My Movie1",
                "description": "string",
                "watched": False,
            },
        ),
    ],
)
async def test_create_movie_validations(test_client, movie_json):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = partial(memory_movie_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    # Test
    result = test_client.post("/api/v1/movie/", json=movie_json)

    # Assert
    assert result.status_code == 422


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movies_seed, movie_id, expected_status_code, expected_result",
    [
        pytest.param(
            [],
            "non-existent ID",
            404,
            {"message": "Movie with ID non-existent ID not found."},
            id="non-existent ID",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID12",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID13",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            "valid-ID12",
            200,
            {
                "description": "test description",
                "id": "valid-ID12",
                "release_year": 1999,
                "title": "test movie",
                "watched": False,
            },
            id="valid ID",
        ),
    ],
)
async def test_get_movie_by_id(
    test_client, movies_seed, movie_id, expected_status_code, expected_result
):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = partial(memory_movie_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    # Test
    for movie in movies_seed:
        await repo.create(movie)

    # Assert
    result = test_client.get(f"/api/v1/movie/{movie_id}")
    assert result.status_code == expected_status_code
    assert result.json() == expected_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movies_seed, skip, limit, expected_status_code, expected_result",
    [
        pytest.param([], 0, 0, 200, [], id="Skip 0, Limit 0, No movies"),
        pytest.param(
            [
                Movie(
                    id="valid-ID13",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            0,
            0,
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID13",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID14",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
            ],
            id="Skip 0, Limit 0, valid movies",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID13",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID15",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID16",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            0,
            1,
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID13",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                }
            ],
            id="Skip 0, Limit 1, valid movies",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID13",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID15",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID16",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            1,
            1,
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID14",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                }
            ],
            id="Skip 1, Limit 1, valid movies",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID13",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID15",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID16",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            1,
            2,
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID14",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID15",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
            ],
            id="Skip 1, Limit 2, valid movies",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID13",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID15",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID16",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            0,
            1000,
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID13",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID14",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID15",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID16",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
            ],
            id="Skip 1, Limit 2, valid movies",
        ),
    ],
)
async def test_get_all(
    test_client, movies_seed, skip, limit, expected_status_code, expected_result
):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = partial(memory_movie_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency
    # Test
    for movie in movies_seed:
        await repo.create(movie)
    result = test_client.get(f"/api/v1/movie/all?skip={skip}&limit={limit}")
    # Assert
    assert result.status_code == expected_status_code
    for movie in result.json():
        assert movie in expected_result
    assert len(result.json()) == len(expected_result)


@pytest.mark.parametrize(
    "movies_seed, skip, limit, title, expected_status_code, expected_result",
    [
        pytest.param(
            [],
            0,
            1000,
            "",
            422,
            {
                "detail": [
                    {
                        "ctx": {"limit_value": 2},
                        "loc": ["query", "title"],
                        "msg": "ensure this value has at least 2 characters",
                        "type": "value_error.any_str.min_length",
                    }
                ]
            },
            id="empty title",
        ),
        pytest.param(
            [],
            0,
            1000,
            "invalid-title",
            404,
            {"message": f'No movies titled "invalid-title" were found.'},
            id="valid title, no movies sent",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID15",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID16",
                    title="test movie1",
                    description="test description",
                    release_year=1999,
                ),
            ],
            0,
            1000,
            "test movie",
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID14",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID15",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
            ],
            id="valid title, movies sent",
        ),
        pytest.param(
            [
                Movie(
                    id="valid-ID14",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID15",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
                Movie(
                    id="valid-ID16",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                ),
            ],
            1,
            2,
            "test movie",
            200,
            [
                {
                    "description": "test description",
                    "id": "valid-ID15",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
                {
                    "description": "test description",
                    "id": "valid-ID16",
                    "release_year": 1999,
                    "title": "test movie",
                    "watched": False,
                },
            ],
            id="valid title, movies sent",
        ),
    ],
)
@pytest.mark.asyncio()
async def test_get_movie_by_title(
    test_client, movies_seed, skip, limit, title, expected_status_code, expected_result
):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = partial(memory_movie_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency

    # Test
    for movie in movies_seed:
        await repo.create(movie)
    result = test_client.get(f"/api/v1/movie/?title={title}&skip={skip}&limit={limit}")

    # Assert
    assert result.status_code == expected_status_code
    for movie in result.json():
        assert movie in expected_result
    assert len(result.json()) == len(expected_result)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movies_seed, movie_id, update_parameters, expected_status_code, expected_result",
    [
        pytest.param(
            [
                Movie(
                    id="valid_ID1",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                )
            ],
            "valid_ID1",
            {
                "description": "test description updated",
                "release_year": 2000,
                "title": "updated test movie",
                "watched": True,
            },
            200,
            {
                "description": "test description updated",
                "id": "valid_ID1",
                "release_year": 2000,
                "title": "updated test movie",
                "watched": True,
            },
            id="no updates",
        )
    ],
)
async def test_patch_update(
    test_client,
    movies_seed,
    movie_id,
    update_parameters,
    expected_status_code,
    expected_result,
):

    # Test
    for movie in movies_seed:
        await repo.create(movie)
    update_result = test_client.patch(
        f"/api/v1/movie/{movie_id}", json=update_parameters
    )
    read_result = test_client.get(f"/api/v1/movie/valid_ID1")

    # Assert
    assert update_result.status_code == expected_status_code
    assert update_result.json() == {"message": "Movie valid_ID1 updated."}
    assert read_result.json() == expected_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "movies_seed, movie_id, expected_status_code, expected_result",
    [
        pytest.param(
            [
                Movie(
                    id="valid_ID1",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                )
            ],
            "valid_ID1",
            204,
            "",
            id="valid movie successfully deleted",
        ),
        pytest.param(
            [
                Movie(
                    id="valid_ID1",
                    title="test movie",
                    description="test description",
                    release_year=1999,
                )
            ],
            "valid_ID2",
            204,
            "",
            id="valid movie successfully deleted",
        ),
    ],
)
async def test_delete(
    test_client, movies_seed, movie_id, expected_status_code, expected_result
):
    # Setup
    repo = MemoryMovieRepository()
    patched_dependency = partial(memory_movie_repository_dependency, repo)

    test_client.app.dependency_overrides[movie_repository] = patched_dependency

    # Test
    for movie in movies_seed:
        await repo.create(movie)

    delete_result = test_client.delete(f"/api/v1/movie/{movie_id}")
    read_result = test_client.get(f"/api/v1/movie/{movie_id}")

    # Assert
    assert delete_result.status_code == expected_status_code
    assert read_result.json() == {"message": f"Movie with ID {movie_id} not found."}
