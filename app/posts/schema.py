

from pydantic import BaseModel, Field, field_validator


class PostCreateRequest(BaseModel):
    post_id: int = Field(1, gt=0)
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Content can not be empty!")
        return value


class PostCreateResponse(BaseModel):
    post_id: int
    content: str


class PostPath(BaseModel):
    post_id: int = Field(gt=0)


class PostUpdateRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Content can not be empty!")
        return value


class PostUpdateResponse(BaseModel):
    post_id: int
    content: str
