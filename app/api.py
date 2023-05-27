from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from app.handlers import movie_v1


def create_app():
    app = FastAPI(title="Movie Tracker", docs_url="/")

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Instrumentator().instrument(app).expose(app)

    app.include_router(movie_v1.router)

    app = VersionedFastAPI(app, version_format="{major}", prefix_format="/api/v{major}")

    return app
