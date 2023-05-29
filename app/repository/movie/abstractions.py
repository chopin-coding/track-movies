import abc
import typing

from app.entities.movie import Movie


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    async def create(self, movie: Movie) -> bool:
        """Inserts movie to DB."""
        raise NotImplementedError

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """Retrieves a movie by its ID"""
        raise NotImplementedError

    async def get_by_fields(
        self,
        title: str = None,
        release_year: int = None,
        watched: bool = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> tuple[list[Movie], int]:
        """Returns a list of movies that share the same title."""

        raise NotImplementedError

    async def update(self, movie_id: str, update_parameters: dict):
        """Update a movie by ID."""

        raise NotImplementedError

    async def delete(self, movie_id: str) -> bool:
        """Deletes a movie by ID."""

        raise NotImplementedError
