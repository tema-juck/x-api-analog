from itertools import count
from typing import Annotated

from fastapi import APIRouter, Path

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostDeleteRespone,
    PostUpdateRequest,
    PostUpdateResponse,
)

router = APIRouter(prefix="/v1/posts", tags=["Posts"])
PostId = Annotated[int, Path(gt=0)]
_post_ids = count(1)


@router.get("/{post_id}", summary="Get a post ID")
def get_id(post_id: PostId) -> dict:
    return {"post_id": post_id}


@router.post("/create_post", response_model=PostCreateResponse, summary="Create a post")
async def create_post(post: PostCreateRequest) -> PostCreateResponse:
    return PostCreateResponse(post_id=next(_post_ids), content=post.content)


@router.patch("/{post_id}", response_model=PostUpdateResponse, summary="Update a post")
async def update_post(post_id: PostId, data: PostUpdateRequest):
    return PostUpdateResponse(post_id=post_id, content=data.content)


@router.delete("/{post_id}", response_model=PostDeleteRespone, summary="Delete a post")
async def delete_post(post_id: PostId): ...
