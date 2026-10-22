from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostPath,
    PostResponse,
    PostSearchParams,
    PostSearchResponse,
    PostUpdateRequest,
)
from .service import PostServiceDeps

router = APIRouter(prefix="/v1/posts", tags=["Posts"])
PostId = Annotated[int, Path(gt=0)]


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Get a post by id",
    description="""This endpoint helps you to get a post by id""",
)
async def get_post(
    service: PostServiceDeps,
    path: PostPath = Depends(),  # noqa: B008
):
    post = await service.get(path.post_id)
    if post is None:
        raise HTTPException(404, "Post not found!")

    if post.is_deleted:
        raise HTTPException(404, "Post is deleted!")

    return PostResponse(
        post_id=post.post_id,
        content=post.content,
        likes_count=post.likes_count,
        is_deleted=post.is_deleted,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.post(
    "/",
    response_model=PostCreateResponse,
    summary="Create a post",
    description="""This endpoint helps you to create a post""",
)
async def create_post(
    service: PostServiceDeps, data: PostCreateRequest
) -> PostCreateResponse:
    res = await service.create(data)
    return PostCreateResponse(
        post_id=res.post_id, content=res.content, likes_count=res.likes_count
    )


@router.patch(
    "/{post_id}",
    response_model=PostResponse,
    summary="Update a post by id",
    description="""This endpoint helps you to update a post by id""",
)
async def update_post(
    data: PostUpdateRequest,
    service: PostServiceDeps,
    path: PostPath = Depends(),  # noqa: B008
):
    post = await service.update(path.post_id, data)
    if post is None:
        raise HTTPException(404, "Post not found!")
    if post.is_deleted:
        raise HTTPException(404, "Post is deleted!")
    return PostResponse(
        post_id=post.post_id,
        content=post.content,
        likes_count=post.likes_count,
        is_deleted=post.is_deleted,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.delete(
    "/{post_id}",
    summary="Delete a post by id",
    description="""This endpoint helps you to delete a post by id""",
)
async def delete_post(
    service: PostServiceDeps,
    path: PostPath = Depends(),  # noqa: B008
):
    post = await service.soft_delete(path.post_id)
    if post is None:
        raise HTTPException(404, "Post not found!")


@router.get(
    "/",
    response_model=PostSearchResponse,
    summary="Search posts",
    description="""This endpoint helps you to search a post""",
)
async def search_post(
    service: PostServiceDeps,
    params: PostSearchParams = Depends(),  # noqa: B008
):
    posts, total, deleted = await service.search(params)
    return PostSearchResponse(
        items=[
            PostResponse(
                post_id=p.post_id,
                content=p.content,
                likes_count=p.likes_count,
                is_deleted=p.is_deleted,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in posts
        ],
        total=total,
        deleted=deleted,
        limit=params.limit,
        offset=params.offset,
    )


@router.patch(
    "/like/{post_id}",
    response_model=PostResponse,
    summary="Update a post by id",
    description="""This endpoint helps you to update a post by id""",
)
async def like_post(
    service: PostServiceDeps,
    path: PostPath = Depends(),  # noqa: B008
):
    post = await service.like(path.post_id)

    if post is None:
        raise HTTPException(404, "Post not found!")

    return PostResponse(
        post_id=post.post_id,
        content=post.content,
        likes_count=post.likes_count,
        is_deleted=post.is_deleted,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )
