import typing

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from fastapi_versioning import versioned_api_route

from app.dto.detail import DetailResponse
from app.dto.movie import (
    MovieResponse,
)
from app.repository.movie.abstractions import MovieRepository
from app.handlers.handler_dependencies import movie_repository, pagination_params

router = APIRouter(
    prefix="/movie",
    tags=["movies"],
    route_class=versioned_api_route(2)
)

@router.get("/all", response_model=typing.List[MovieResponse])
async def get_all(
    repo: MovieRepository = Depends(movie_repository),
    pagination=Depends(pagination_params),
):
    """Returns all the movies in the database."""

    movies = await repo.get_all(skip=pagination.skip, limit=pagination.limit)
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
    # FIXME: Gotta find a way to avoid iterating through the results to create MovieResponse objects individually
    #  while keeping Pydantic happy.
    return movies_returned


@router.get(
    "/{movie_id}",
    responses={200: {"model": MovieResponse}, 404: {"model": DetailResponse}},
)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(movie_repository)
):
    """Returns a movie if it exists, None if not."""

    movie = await repo.get_by_id(movie_id=movie_id)
    if movie is None:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message=f"Movie with ID {movie_id} not found.")
            ),
        )
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
    pagination=Depends(pagination_params),
):
    """Returns movie by title."""

    movies = await repo.get_by_title(
        title=title, skip=pagination.skip, limit=pagination.limit
    )
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
    if not movies_returned:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                DetailResponse(message=f'No movies titled "{title}" were found.')
            ),
        )
    return movies_returned

