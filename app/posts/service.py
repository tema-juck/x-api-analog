from typing import Annotated

from fastapi import Depends

from app.posts.model import Post
from app.posts.schema import PostCreateRequest, PostSearchParams, PostUpdateRequest

from .repository import PostRepository, PostRepositoryDeps


def get_post_service(repo: PostRepositoryDeps):
    return PostService(repo)


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def get(self, post_id: int):
        return await self.repo.get_by_id(post_id)

    async def create(self, data: PostCreateRequest):
        task = Post(content=data.content)
        return await self.repo.save(task)

    async def update(self, post_id: int, data: PostUpdateRequest):
        post = await self.repo.get_by_id(post_id)

        if post is None:
            return None

        if post.is_deleted:
            return None

        patch = data.model_dump(exclude_unset=True)
        for field, value in patch.items():
            setattr(post, field, value)

        return await self.repo.save(post)

    async def soft_delete(self, post_id: int):
        post = await self.repo.get_by_id(post_id)

        if post is None:
            return None

        if post.is_deleted:
            return None

        post.is_deleted = True
        return await self.repo.save(post)

    async def search(self, params: PostSearchParams) -> tuple[list[Post], int, int]:
        return await self.repo.search(
            offset=params.offset, limit=params.limit, post_id=params.post_id
        )

    async def like(self, post_id: int):
        post = await self.repo.like(post_id)

        if post is None:
            return None

        if post.is_deleted:
            return None

        return post


PostServiceDeps = Annotated[PostService, Depends(get_post_service)]
