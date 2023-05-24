from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from app.api.handlers import movie_v1


def create_app():
    app = FastAPI(docs_url="/")

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Instrumentator().instrument(app).expose(app)
    # app.add_middleware(CustomHeaderMiddleware, test_option=True)

    # Routers
    # app.include_router(demo.router) # practice
    # app.include_router(responses_section.router) # practice
    app.include_router(movie_v1.router)

    return app
