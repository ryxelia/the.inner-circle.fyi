from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from ticfyi.templates import templates


__all__: tuple[str, ...] = (
    "app",
)


def add_routes(app: FastAPI) -> None:
    from ticfyi.router import router as root_router
    from ticfyi.routers.ring import router as ring_router
    app.include_router(root_router)
    app.include_router(ring_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    templates.load()
    app.mount(
        "/static",
        StaticFiles(directory="_served/static"),
        name="static",
    )
    add_routes(app)
    yield


app = FastAPI(
    debug=False,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
    summary="",
    lifespan=lifespan,
    title="the.inner-circle.fyi",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)
