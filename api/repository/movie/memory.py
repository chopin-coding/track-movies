import typing

from api.entities.movie import Movie
from api.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)


class MemoryMovieRepository(MovieRepository):
    """
    MemoryMovieRepository implements the repository pattern by using a simple in memory database.
    """

    def __init__(self):
        self._storage = {}

    async def create(self, movie: Movie):
        self._storage[movie.id] = movie

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
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
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"movie {movie_id} not found")
        for key, value in update_parameters.items():
            if key == "id":
                raise RepositoryException(f"can't update movie ID")
            # Check that update_parameters are fields in the Movie entities
            if hasattr(movie, key):
                # Update the Movie entities field
                setattr(movie, f"_{key}", value)

    async def delete(self, movie_id: str):  # removed inferred return type bool
        self._storage.pop(movie_id, None)
