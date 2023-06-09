from collections import namedtuple
from functools import lru_cache

from fastapi import Depends, Query

from app.config import Settings, settings_instance
from app.repository.movie.abstractions import MovieRepository
from app.repository.movie.mongo import MongoMovieRepository


def _make_movie_repository(settings: Settings) -> MovieRepository:
    """Movie repository instance to be used as a FastAPI dependency."""

    return MongoMovieRepository(
        connection_string=settings.mongo_connection_string,
        database=settings.mongo_database_name,
        server_selection_timeout_ms=settings.server_selection_timeout_ms,
    )


def movie_repository(settings: Settings = Depends(settings_instance)):
    """Workaround function to cache _make_movie_repository()."""

    @lru_cache()
    def cache():
        return _make_movie_repository(settings)

    return cache()


def pagination_params(
    skip: int = Query(
        0, title="Skip", description="The number of results to be skipped.", ge=0
    ),
    limit: int = Query(
        1000, title="Limit", description="The maximum number of results to be returned."
    ),
):
    """Returns a namedtuple consisting of skip and limit for pagination."""

    Pagination = namedtuple("Pagination", ["skip", "limit"])
    return Pagination(skip=skip, limit=limit)
