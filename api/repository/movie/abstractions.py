import abc
import typing

from api.entity.movie import Movie


# CRUD
# C - Create
# R - Read
# U - Update
# D - Delete


class RepositoryException(Exception):
    ...


class MovieRepository(abc.ABC):
    def create(self, movie: Movie) -> bool:
        """
        Creates a movie and returns True on success.

        Raises RepositoryException on failure.
        """
        raise NotImplementedError

    def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """
        Retrieves a movie by its ID. Returns None if the movie is not found.
        """
        raise NotImplementedError

    def get_by_title(self, movie_id: str) -> typing.List[Movie]:
        """
        Returns a list of movies that share the same title.
        """
        raise NotImplementedError

    def update(self, movie_id: str):
        """
        Update a movie by ID.
        """
        raise NotImplementedError

    def delete(self, movie_id: str) -> bool:
        """
        Deletes a movie by ID.

        Raises RepositoryException on failure.
        """
        raise NotImplementedError
