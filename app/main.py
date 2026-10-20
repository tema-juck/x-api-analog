from fastapi import FastAPI

from app.core.settings import Settings
from app.posts.routes import router as post_router


def create_app() -> FastAPI:
    settings = Settings()  # type: ignore[call-arg]
    new_app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        openapi_tags=settings.app.openapi_tags,
    )
    new_app.state.settings = settings

    new_app.include_router(post_router)

    return new_app


app = create_app()
