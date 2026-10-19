from pydantic import BaseModel, Field, field_validator


class PostPath(BaseModel):
    post_id: int = Field(gt=0)


class PostBase(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Content can not be empty!")
        return value


class PostResponse(BaseModel):
    post_id: int


class PostCreateRequest(PostBase):
    pass


class PostCreateResponse(BaseModel):
    post_id: int
    content: str


class PostUpdateRequest(PostBase):
    pass


class PostUpdateResponse(BaseModel):
    post_id: int
    content: str


class PostDeleteRespone(BaseModel):
    post_id: int
