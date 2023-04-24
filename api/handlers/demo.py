from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

from api.DTO.detail import DetailResponse

router = APIRouter(prefix="/api/v1/demo")


class NameIn(BaseModel):
    name: str
    prefix: str = "Mr."


@router.get("/", response_model=DetailResponse)
def hello_world():
    """
    This is the hello world endpoint.
    """
    return DetailResponse(message="Hello World")


@router.get("/hello", response_model=DetailResponse)
def send_data_query(name: str = Query(..., title="Name", description="The name")):
    return DetailResponse(message=f"Hello {name}")


@router.post("/hello/name", response_model=DetailResponse)
def send_data_body(name: NameIn):
    """
    Response with Hello name where name is provided by the user
    """
    return DetailResponse(message=f"Hello {name.prefix} {name.name}")


@router.post("/hello/{name}", response_model=DetailResponse)
def send_data_path(name: str = Path(..., title="Name")):
    """
    Response with Hello name where name is provided by the user
    """
    return DetailResponse(message=f"Hello {name}")


@router.delete("/delete", response_model=DetailResponse)
def delete_data():
    return DetailResponse(message=f"Data deleted")


@router.delete(
    "/delete/{name}",
    response_model=DetailResponse,
    responses={404: {"model": DetailResponse}},
)
def delete_data(name: str):
    if name == "admin":
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(DetailResponse(message="Can't delete admin")),
        )
    return DetailResponse(message=f"{name} deleted")


@router.get(
    "/error", response_model=DetailResponse, responses={404: {"model": DetailResponse}}
)
def get_error_http():
    raise HTTPException(404, detail="This endpoint always fails.")
