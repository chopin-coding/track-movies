import typing

from app.entities.movie import Movie
from app.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)


class MemoryMovieRepository(MovieRepository):
    """Implements the repository pattern through an in memory database."""

    def __init__(self):
        self._storage = {}

    async def create(self, movie: Movie):
        """Inserts movie to DB."""

        self._storage[movie.id] = movie

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """Retrieves a movie by its ID.

        Returns None if the movie is not found.
        """

        return self._storage.get(movie_id)

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        """Returns the list of movies that share the same title."""

        matched = []
        for _, value in self._storage.items():
            if title == value.title:
                matched.append(value)
        if limit == 0:
            return matched[skip:]
        return matched[skip : skip + limit]

    async def get_all(self, skip: int = 0, limit: int = 1000) -> typing.List[Movie]:
        if limit == 0:
            all_movies = list(self._storage.values())[skip:]
            return all_movies
        all_movies = list(self._storage.values())[skip : skip + limit]
        return all_movies

    async def update(self, movie_id: str, update_parameters: dict):
        """Update a movie by ID.

        Parameters
        ----------
        movie_id: str
        update_parameters: dict
            Desired Movie fields and their values.

        Raises
        ------
        RepositoryException
            If movie ID update attempted.
        """

        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"movie {movie_id} not found")
        for key, value in update_parameters.items():
            if key == "id":
                raise RepositoryException(f"can't update movie ID")
            if hasattr(movie, key):
                setattr(movie, key, value)

    async def delete(self, movie_id: str):
        """Deletes a movie by ID."""

        self._storage.pop(movie_id, None)
