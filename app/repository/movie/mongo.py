import typing

import motor.motor_asyncio

from app.dto.detail import DetailResponse
from app.entities.movie import Movie
from app.repository.movie.abstractions import (MovieRepository,
                                               RepositoryException)


class MongoMovieRepository(MovieRepository):
    """Implements the repository pattern using MongoDB."""

    def __init__(
        self,
        connection_string: str,
        database: str,
    ):
        """Initialize using the env variables passed."""

        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        """Upserts a movie to the DB."""

        await self._movies.update_one(
            {"id": movie.id},
            {
                "$set": {
                    "id": movie.id,
                    "title": movie.title,
                    "description": movie.description,
                    "release_year": movie.release_year,
                    "watched": movie.watched,
                }
            },
            upsert=True,
        )

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        """Retrieves a movie by its ID.

        Returns None if the movie is not found.
        """
        document = await self._movies.find_one({"id": movie_id})
        if document:
            return Movie(
                id=document.get("id"),
                title=document.get("title"),
                description=document.get("description"),
                release_year=document.get("release_year"),
                watched=document.get("watched"),
            )
        return None

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        """Returns the list of movies sharing the given title."""

        return_value: typing.List[Movie] = []
        document_cursor = self._movies.find({"title": title}).skip(skip).limit(limit)
        async for document in document_cursor:
            return_value.append(
                Movie(
                    id=document.get("id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    release_year=document.get("release_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

    async def get_all(self, skip: int = 0, limit: int = 1000) -> typing.List[Movie]:
        return_value: typing.List[Movie] = []
        documents = self._movies.find().skip(skip).limit(limit)
        async for document in documents:
            return_value.append(
                Movie(
                    id=document.get("id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    release_year=document.get("release_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

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

        RepositoryException
            If movie ID not found.
        """

        if "id" in update_parameters.keys():
            raise RepositoryException("can't update movie ID")
        result = await self._movies.update_one(
            {"id": movie_id}, {"$set": update_parameters}
        )
        if result.matched_count == 0:
            raise RepositoryException(f'movie with ID "{movie_id}" not found.')

    async def delete(self, movie_id: str):
        """Deletes a movie by ID."""

        result = await self._movies.delete_one({"id": movie_id})
