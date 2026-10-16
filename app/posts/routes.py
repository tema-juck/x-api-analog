from itertools import count
from typing import Annotated

from fastapi import APIRouter, Path

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostUpdateRequest,
    PostUpdateResponse,
)

router = APIRouter()
PostId = Annotated[int, Path(gt=0)]
_post_ids = count(1)


@router.get("/{post_id}")
def get_id(post_id: PostId) -> dict:
    return {"post_id": post_id}


@router.post("/create_post")
async def create_post(post: PostCreateRequest) -> PostCreateResponse:
    return PostCreateResponse(post_id=next(_post_ids), content=post.content)


@router.patch("/{post_id}")
async def update_post(post_id: PostId, data: PostUpdateRequest):
    return PostUpdateResponse(post_id=post_id, content=data.content)


@router.delete("/{post_id}")
async def delete_post(post_id: PostId): ...
