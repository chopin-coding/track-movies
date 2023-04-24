import abc
import typing

from api.entities.movie import Movie

# CRUD
# C - Create
# R - Read
# U - Update
# D - Delete


class RepositoryException(Exception):
    pass


class MovieRepository(abc.ABC):
    async def create(self, movie: Movie) -> bool:
        """
        Inserts movie to DB.

        Raises RepositoryException on failure.
        """
        raise NotImplementedError

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """
        Retrieves a movie by its ID. Returns None if the movie is not found.
        """
        raise NotImplementedError

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        """
        Returns a list of movies that share the same title.
        """
        raise NotImplementedError

    async def get_all(self, skip: int = 0, limit: int = 1000) -> typing.List[Movie]:
        """
        Returns the list of all the movies in the DB.
        """
        raise NotImplementedError

    async def update(self, movie_id: str, update_parameters: dict):
        """
        Update a movie by ID.
        """
        raise NotImplementedError

    async def delete(self, movie_id: str) -> bool:
        """
        Deletes a movie by ID.

        Raises RepositoryException on failure.
        """
        raise NotImplementedError
