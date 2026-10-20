import logging.config
from pathlib import Path

import yaml
from fastapi import FastAPI

from app.core.settings import Settings
from app.posts.routes import router as post_router


def create_app() -> FastAPI:
    config_path = Path(__file__).resolve().parents[1] / "log_conf.yaml"

    with config_path.open(encoding="utf-8") as file:
        log_config = yaml.safe_load(file)

    logging.config.dictConfig(log_config)

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
