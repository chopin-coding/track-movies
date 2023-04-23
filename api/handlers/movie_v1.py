import typing
import uuid
from functools import lru_cache

from fastapi import APIRouter, Body, Depends, Query

from api.dto.movie import CreateMovieBody
from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository
from api.repository.movie.mongo import MongoMovieRepository
from api.responses.detail import DetailResponse
from api.responses.movie import MovieCreatedResponse, MovieResponse
from api.settings import Settings, settings_instance

router = APIRouter(prefix="/api/v1/movie", tags=["movies"])


def _make_movie_repository(settings: Settings) -> MovieRepository:
    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
    )


def movie_repository(settings: Settings = Depends(settings_instance)):
    """
    Movie repository instance to be used as a FastAPI dependency.
    """

    @lru_cache()
    def cache():
        return _make_movie_repository(settings)

    return cache()


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def post_create_movie(
    movie: CreateMovieBody = Body(..., title="Movie", description="The movie details"),
    repo: MovieRepository = Depends(movie_repository),
):
    """
    Creates a movie.
    """

    movie_id = str(uuid.uuid4())

    await repo.create(
        movie=Movie(
            movie_id=movie_id,
            title=movie.title,
            description=movie.description,
            release_year=movie.release_year,
            watched=movie.watched,
        )
    )
    return MovieCreatedResponse(id=movie_id)


@router.get("/all", response_model=typing.List[MovieResponse])
async def get_all(
    repo: MovieRepository = Depends(movie_repository),
):
    movies = await repo.get_all()
    movies_returned = []
    for movie in movies:
        movies_returned.append(
            MovieResponse(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                release_year=movie.release_year,
                watched=movie.watched,
            )
        )
    return movies_returned


@router.get(
    "/{movie_id}",
    responses={200: {"model": MovieResponse}, 404: {"model": DetailResponse}},
)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(movie_repository)
):
    """
    Returns a movie if it exists, None if not.
    """
    movie = await repo.get_by_id(movie_id=movie_id)
    if movie is None:
        return DetailResponse(message=f"Movie with ID {movie_id} not found.")
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        release_year=movie.release_year,
        watched=movie.watched,
    )


@router.get("/", response_model=typing.List[MovieResponse])
async def get_movie_by_title(
    title: str = Query(
        ..., title="Title", description="The title of the movie.", min_length=2
    ),
    repo: MovieRepository = Depends(movie_repository),
):
    movies = await repo.get_by_title(title)
    movies_returned = []
    for movie in movies:
        movies_returned.append(
            MovieResponse(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                release_year=movie.release_year,
                watched=movie.watched,
            )
        )
    return movies_returned
