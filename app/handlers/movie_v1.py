import typing
import uuid

from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import versioned_api_route
from pymongo.errors import PyMongoError
from starlette.responses import JSONResponse, Response

from app.dto.detail import DetailResponse
from app.dto.movie import (
    CreateMovieBody,
    MovieCreatedResponse,
    MovieResponse,
    MovieUpdateBody,
    MovieResponseWithCount,
)
from app.entities.movie import Movie
from app.handlers.handler_dependencies import movie_repository, pagination_params
from app.repository.movie.abstractions import MovieRepository, RepositoryException

router = APIRouter(prefix="/movie", tags=["movies"], route_class=versioned_api_route(1))


@router.post("/", status_code=201, response_model=MovieCreatedResponse)
async def post_create_movie(
    movie: CreateMovieBody = Body(..., title="Movie", description="The movie details"),
    repo: MovieRepository = Depends(movie_repository),
):
    """Creates a movie."""

    try:
        movie_id = str(uuid.uuid4())

        await repo.create(
            movie=Movie(
                id=movie_id,
                title=movie.title,
                description=movie.description,
                release_year=movie.release_year,
                watched=movie.watched,
            )
        )
        return MovieCreatedResponse(id=movie_id)
    except PyMongoError as _:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                DetailResponse(
                    message=str(
                        "The database is currently unreachable. Please try again later."
                    )
                )
            ),
        )


@router.get(
    "/{movie_id}",
    responses={200: {"model": MovieResponse}, 404: {"model": DetailResponse}},
)
async def get_movie_by_id(
    movie_id: str, repo: MovieRepository = Depends(movie_repository)
):
    """Returns a movie if it exists, 404 if not."""

    try:
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
    except PyMongoError as _:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                DetailResponse(
                    message=str(
                        "The database is currently unreachable. Please try again later."
                    )
                )
            ),
        )


@router.get(
    "/",
    responses={
        200: {"model": typing.List[MovieResponse]},
        404: {"model": DetailResponse},
        500: {"model": DetailResponse},
    },
)
async def get_movie_by_fields(
    title: str
    | None = Query(
        None, title="Title", description="The title of the movie.", min_length=2
    ),
    release_year: int
    | None = Query(
        None,
        title="Release Year",
        description="The release year of the movie.",
        gt=1894,
    ),
    watched: bool
    | None = Query(
        None, title="Watched", description="Whether the movie is watched or not"
    ),
    repo: MovieRepository = Depends(movie_repository),
    pagination=Depends(pagination_params),
):
    """Returns the list of movies with the matching search parameters
     and their total count regardless of pagination.

    Returns the list of all movies if no search parameters are given.
    """

    try:
        movies, total_count = await repo.get_by_fields(
            title=title,
            release_year=release_year,
            watched=watched,
            skip=pagination.skip,
            limit=pagination.limit,
        )
        movies_to_return = []
        for movie in movies:
            movies_to_return.append(
                MovieResponse(
                    id=movie.id,
                    title=movie.title,
                    description=movie.description,
                    release_year=movie.release_year,
                    watched=movie.watched,
                )
            )
        if not movies_to_return:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder(
                    DetailResponse(
                        message="No movies with the given parameters were found."
                    )
                ),
            )
        response = MovieResponseWithCount(movies=movies_to_return, count=total_count)
        return response
    except PyMongoError as _:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                DetailResponse(
                    message=str(
                        "The database is currently unreachable. Please try again later."
                    )
                )
            ),
        )


@router.patch(
    "/{movie_id}",
    responses={200: {"model": DetailResponse}, 400: {"model": DetailResponse}},
)
async def update(
    movie_id: str,
    update_parameters: MovieUpdateBody = Body(
        ..., title="Update body", description="The movie update parameters"
    ),
    repo: MovieRepository = Depends(movie_repository),
):
    """Update a movie by ID.

    Parameters
    ----------
    movie_id: str
    update_parameters: dict
        Desired Movie fields and their values.
    repo: MovieRepository
        The repo to be used; In-memory or MongoDB.

    Returns
    ------
    HTTP 200
        If movie update successful.

    HTTP 200
        If update parameters match the existing movie data.

    HTTP 400
        If movie ID not found.
    """

    try:
        await repo.update(
            movie_id=movie_id,
            update_parameters=update_parameters.dict(
                exclude_unset=True, exclude_none=True
            ),
        )
        return DetailResponse(message=f"Movie with ID {movie_id} updated.")

    except RepositoryException as e:
        return JSONResponse(
            status_code=400, content=jsonable_encoder(DetailResponse(message=str(e)))
        )
    except PyMongoError as _:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                DetailResponse(
                    message=str(
                        "The database is currently unreachable. Please try again later."
                    )
                )
            ),
        )


@router.delete("/{movie_id}", status_code=204)
async def delete(movie_id: str, repo: MovieRepository = Depends(movie_repository)):
    """Deletes a movie by ID.

    Returns
    ------
    HTTP 204
        If the movie was deleted successfully.

    HTTP 204
        If the movie ID was not found.
    """

    try:
        await repo.delete(movie_id=movie_id)
        return Response(status_code=204)
    except PyMongoError as _:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                DetailResponse(
                    message=str(
                        "The database is currently unreachable. Please try again later."
                    )
                )
            ),
        )
