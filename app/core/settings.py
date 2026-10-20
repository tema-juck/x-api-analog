from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, Request
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSetting(BaseModel):
    name: str = "X-Analog API"
    description: str = "API for pet-project"
    version: str = "0.1.0"
    openapi_tags: list[dict] = [{"name": "Posts", "description": "Control your Posts"}]


class DatabaseSetting(BaseModel):
    url: str


class AuthSetting(BaseModel):
    jwt_secret: str


class DebounceSetting(BaseModel):
    minimal_post_debounce_time: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    database_url: str
    jwt_secret: str
    minimal_post_debounce_time: int

    @property
    def app(self) -> AppSetting:
        return AppSetting()

    @property
    def db(self) -> DatabaseSetting:
        return DatabaseSetting(url=self.database_url)

    @property
    def auth(self) -> AuthSetting:
        return AuthSetting(jwt_secret=self.jwt_secret)

    @property
    def debounce(self) -> DebounceSetting:
        return DebounceSetting(
            minimal_post_debounce_time=self.minimal_post_debounce_time
        )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        parsed = urlparse(value)

        if parsed.scheme not in {"postgresql", "postgresql+asyncpg"}:
            raise ValueError(
                "database_url scheme must be postgresql or postgresql+asyncpg"
            )

        if not parsed.hostname:
            raise ValueError("database_url must include hostname")

        dbname = (parsed.path or "").lstrip("/")
        if not dbname:
            raise ValueError("database_url name must include database")

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("database_url port must be 1..65535")

        return value


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


SettingsDeps = Annotated[Settings, Depends(get_settings)]
