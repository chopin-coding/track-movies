from pydantic import BaseModel


class MovieCreatedResponse(BaseModel):
    id: str


class MovieResponse(MovieCreatedResponse):
    title: str
    description: str
    release_year: int
    watched: bool = False
