import typing

from pydantic import BaseModel, validator


class CreateMovieBody(BaseModel):
    """
    CreateMovieBody is used as the body for the create movie endpoint.
    """

    title: str
    description: str
    release_year: int
    watched: bool = False

    @validator("title")
    def title_length_gt_one(cls, v):
        if len(v) < 2:
            raise ValueError(
                "The movie title length has to be greater than 1 character"
            )
        return v

    @validator("description")
    def description_length_gt_one(cls, v):
        if len(v) < 2:
            raise ValueError(
                "The movie description length has to be greater than 1 character"
            )
        return v

    @validator("release_year")
    def release_year_length_gt_(cls, v):
        if v < 1894:
            raise ValueError("The movie release year has to be after 1893")
        return v


class MovieCreatedResponse(BaseModel):
    id: str


class MovieResponse(MovieCreatedResponse):
    title: str
    description: str
    release_year: int
    watched: bool = False


class MovieUpdateBody(BaseModel):
    # TODO: Implement the validations of the CreateMovieBody class to this class as well, and any other validations that may be necessary.

    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    release_year: typing.Optional[int] = None
    watched: typing.Optional[bool] = None


class MovieDeleteResponse(BaseModel):
    movie_id: str
