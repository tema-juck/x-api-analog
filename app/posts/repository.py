from typing import Annotated

from fastapi import Depends
from sqlalchemy import desc, select, update
from sqlalchemy.sql.functions import count

from app.core.db import DbSessionDeps
from app.posts.model import Post


class PostRepository:
    def __init__(self, session: DbSessionDeps):
        self.session = session

    async def get_by_id(self, post_id: int):
        return await self.session.get(Post, post_id)

    async def save(self, post: Post):
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def search(
        self, offset: int = 0, limit: int = 10, post_id: int | None = None
    ):
        count_query = select(count()).select_from(Post)
        deleted_query = (
            select(count()).select_from(Post).where(Post.is_deleted.is_(True))
        )
        query = select(Post)

        if post_id is not None:
            count_query = count_query.where(Post.post_id == post_id)
            deleted_query = deleted_query.where(Post.post_id == post_id)
            query = query.where(Post.post_id == post_id)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        deleted_result = await self.session.execute(deleted_query)
        deleted_total = deleted_result.scalar_one()

        query = (
            query.order_by(desc(Post.created_at))
            .where(Post.is_deleted.is_(False))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        posts = list(result.scalars().all())
        return posts, total, deleted_total

    async def like(self, post_id: int):
        query = (
            update(Post)
            .where(Post.post_id == post_id, Post.is_deleted.is_(False))
            .values(likes_count=Post.likes_count + 1)
            .returning(Post)
        )

        result = await self.session.execute(query)
        post = result.scalar_one_or_none()
        await self.session.commit()

        return post


def get_post_repository(session: DbSessionDeps):
    return PostRepository(session)


PostRepositoryDeps = Annotated[PostRepository, Depends(get_post_repository)]
