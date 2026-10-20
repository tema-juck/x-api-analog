import logging
from itertools import count
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostDeleteRespone,
    PostPath,
    PostResponse,
    PostUpdateRequest,
    PostUpdateResponse,
)
from .service import PostServiceDeps

router = APIRouter(prefix="/v1/posts", tags=["Posts"])
PostId = Annotated[int, Path(gt=0)]
_post_ids = count(1)

logger = logging.getLogger(__name__)


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Get a post by id",
    description="""This endpoint helps you to get a post by id""",
)
def get_post(
    service: PostServiceDeps,
    path: PostPath = Depends(),  # noqa: B008
):
    res = service.get_post(path.post_id)
    logger.info("ID: %s", res)
    return PostResponse(post_id=res)


@router.post(
    "/create_post",
    response_model=PostCreateResponse,
    summary="Create a post",
    description="""This endpoint helps you to create a post""",
)
async def create_post(post: PostCreateRequest) -> PostCreateResponse:
    return PostCreateResponse(post_id=next(_post_ids), content=post.content)


@router.patch(
    "/{post_id}",
    response_model=PostUpdateResponse,
    summary="Update a post by id",
    description="""This endpoint helps you to update a post by id""",
)
async def update_post(post_id: PostId, data: PostUpdateRequest):
    return PostUpdateResponse(post_id=post_id, content=data.content)


@router.delete(
    "/{post_id}",
    response_model=PostDeleteRespone,
    summary="Delete a post by id",
    description="""This endpoint helps you to delete a post by id""",
)
async def delete_post(post_id: PostId):
    return PostDeleteRespone(post_id=post_id)
