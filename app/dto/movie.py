import typing

from pydantic import BaseModel, validator


class CreateMovieBody(BaseModel):
    """CreateMovieBody is used as the body for the create movie endpoint."""

    title: str
    description: str
    release_year: int
    watched: bool = False

    @validator("title")
    def title_length_gt_one(cls, v):
        if not 221 > len(v) > 2:
            raise ValueError(
                "The movie title should be 2 to 220 characters long."
            )
        return v

    @validator("description")
    def description_length_gt_one(cls, v):
        if not 5001 > len(v) > 2:
            raise ValueError(
                "The movie title should be 2 to 5000 characters long."
            )
        return v

    @validator("release_year")
    def release_year_length_gt_(cls, v):
        if not 2101 > v > 1894:
            raise ValueError("The movie release year should be between 1894 and 2100.")
        return v


class MovieCreatedResponse(BaseModel):
    id: str


class MovieResponse(MovieCreatedResponse):
    title: str
    description: str
    release_year: int
    watched: bool = False


class MovieResponseWithCount(BaseModel):
    movies: list[MovieResponse]
    count: int


class MovieUpdateBody(BaseModel):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    release_year: typing.Optional[int] = None
    watched: typing.Optional[bool] = None

    @validator("title")
    def title_length_gt_one(cls, v):
        if not 221 > len(v) > 2:
            raise ValueError(
                "The movie title should be 2 to 220 characters long."
            )
        return v

    @validator("description")
    def description_length_gt_one(cls, v):
        if not 5001 > len(v) > 2:
            raise ValueError(
                "The movie title should be 2 to 5000 characters long."
            )
        return v

    @validator("release_year")
    def release_year_length_gt_(cls, v):
        if not 2101 > v > 1894:
            raise ValueError("The movie release year should be between 1894 and 2100.")
        return v




class MovieDeleteResponse(BaseModel):
    movie_id: str
