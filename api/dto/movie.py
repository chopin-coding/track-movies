from pydantic import BaseModel, validator


class CreateMovieBody(BaseModel):
    """
    CreateMovieBody is used as the body for the create movie endpoint.
    """

    movie_id: str
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
