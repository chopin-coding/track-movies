import typing

import motor.motor_asyncio

from app.api.entities.movie import Movie
from app.api.repository.movie.abstractions import MovieRepository, RepositoryException


class MongoMovieRepository(MovieRepository):
    """
    MongoMovieRepository implements the repository pattern the Movie entity using MongoDB.
    """

    def __init__(
        self,
        connection_string: str = "mongodb://localhost:27017",
        database: str = "movie_track_db",
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        self._database = self._client[database]
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
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
        document = await self._movies.find_one({"id": movie_id})
        if document:
            return Movie(
                movie_id=document.get("id"),
                title=document.get("title"),
                description=document.get("description"),
                release_year=document.get("release_year"),
                watched=document.get("watched"),
            )
        return None

    async def get_by_title(
        self, title: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Movie]:
        return_value: typing.List[Movie] = []
        document_cursor = self._movies.find({"title": title}).skip(skip).limit(limit)
        async for document in document_cursor:
            return_value.append(
                Movie(
                    movie_id=document.get("id"),
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
                    movie_id=document.get("id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    release_year=document.get("release_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

    async def update(self, movie_id: str, update_parameters: dict):
        if "id" in update_parameters.keys():
            raise RepositoryException("can't update movie ID")
        result = await self._movies.update_one(
            {"id": movie_id}, {"$set": update_parameters}
        )
        if result.matched_count == 0:
            raise RepositoryException(f'movie with ID "{movie_id}" not found.')
        elif result.modified_count == 0:
            raise RepositoryException(
                f'Movie "{movie_id}" was left unchanged because the update parameters matched the existing record.'
            )

    async def delete(self, movie_id: str):
        result = await self._movies.delete_one({"id": movie_id})
        if result.deleted_count == 0:
            raise RepositoryException(f'movie with ID "{movie_id}" not found.')
