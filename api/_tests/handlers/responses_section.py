from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import UJSONResponse
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response, StreamingResponse

from api.DTO.detail import DetailResponse

router = APIRouter(prefix="/api/v1/responses")


@router.get("/json", response_model=DetailResponse)
def hello_world():
    """
    This is the hello world JSON endpoint.
    """
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(DetailResponse(message="Hello world!")),
    )


@router.get("/ujson", response_model=DetailResponse)
def hello_world_ujson():
    """
    This is the hello world Ultra JSON endpoint.
    """
    return UJSONResponse(
        status_code=200,
        content=jsonable_encoder(DetailResponse(message="Hello world!")),
    )


@router.get("/response", response_model=DetailResponse)
def hello_world_response():
    """
    This is the base response endpoint.
    """
    file_path = "/mnt/c/Users/emree/PycharmProjects/movie-tracker-venv/mike_w.jpg"
    with open(file_path, "rb") as file:
        return Response(
            status_code=200, content=file.read(), headers={"Content-Type": "image/jpeg"}
        )


def file_iterator():
    file_path = "/mnt/c/Users/emree/PycharmProjects/movie-tracker-venv/mike_w.jpg"
    with open(file_path, "rb") as file:
        yield from file


@router.get("/streaming", response_model=DetailResponse)
def hello_world_streaming_response():
    """
    This is the streaming endpoint.
    """
    return StreamingResponse(
        status_code=200, content=file_iterator(), headers={"Content-Type": "image/jpeg"}
    )


class PhotoResponse(Response):
    media_type = "image/jpeg"


@router.get("/photo", response_model=DetailResponse)
def hello_world_response():
    """
    This is the base response endpoint.
    """
    file_path = "/mnt/c/Users/emree/PycharmProjects/movie-tracker-venv/mike_w.jpg"
    with open(file_path, "rb") as file:
        return PhotoResponse(
            status_code=200, content=file.read(), headers={"Content-Type": "image/jpeg"}
        )
