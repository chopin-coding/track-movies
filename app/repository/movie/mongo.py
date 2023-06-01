import typing

import motor.motor_asyncio

from app.entities.movie import Movie
from app.repository.movie.abstractions import MovieRepository, RepositoryException, RepositoryMovieNotFoundException


class MongoMovieRepository(MovieRepository):
    """Implements the repository pattern using MongoDB."""

    def __init__(
        self,
        connection_string: str,
        database: str,
        server_selection_timeout_ms: float,
    ):
        """Initialize using the env variables passed."""

        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            connection_string, serverSelectionTimeoutMS=server_selection_timeout_ms
        )
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

    async def get_by_fields(
        self,
        title: str = None,
        release_year: int = None,
        watched: bool = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> tuple[list[Movie], int]:
        """Returns the list of movies with the matching search parameters.

        Returns the list of all movies if no search parameters are given.
        """

        return_value: list[Movie] = []

        search_fields = {
            "title": title,
            "release_year": release_year,
            "watched": watched,
        }.items()

        search_parameters = {
            field: value for field, value in search_fields if value is not None
        }

        total_count_cursor: int = await self._movies.count_documents(search_parameters)
        document_cursor = self._movies.find(search_parameters).skip(skip).limit(limit)
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
        return return_value, total_count_cursor

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
            raise RepositoryMovieNotFoundException(f'movie with ID "{movie_id}" not found.')

    async def delete(self, movie_id: str):
        """Deletes a movie by ID."""

        result = await self._movies.delete_one({"id": movie_id})
