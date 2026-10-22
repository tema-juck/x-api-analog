from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator


class PostPath(BaseModel):
    post_id: int = Field(gt=0)


class PostBase(BaseModel):
    content: str = Field(max_length=280)

    model_config = {"extra": "ignore"}

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Content can not be empty!")
        return value


class PostResponse(BaseModel):
    post_id: int
    content: str
    likes_count: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%d.%m.%Y %H:%M")

    @field_serializer("updated_at")
    def serialize_updated_at(self, value: datetime) -> str:
        return value.strftime("%d.%m.%Y %H:%M")


class PostCreateRequest(PostBase):
    pass


class PostCreateResponse(BaseModel):
    post_id: int
    content: str
    likes_count: int


class PostUpdateRequest(PostBase):
    pass


class PostSearchParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    post_id: int | None = Field(None, gt=0)


class PostSearchResponse(BaseModel):
    items: list[PostResponse]
    total: int
    deleted: int
    limit: int
    offset: int


# class PostLikeRequest(BaseModel):
#     likes_count: int = Field(0, ge=0)
