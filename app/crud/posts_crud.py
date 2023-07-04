from fastapi import Depends
from pydantic.schema import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_session
from app.core.db.models import Posts, Likes, Dislikes
from app.api.request_models.posts import PostsCreateAndUpdateRequest


class PostsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_post(
        self,
        post_id: UUID,
    ) -> Posts:
        """Получить объект поста по id."""
        post = await self.session.execute(
            select(Posts).where(Posts.id == post_id)
        )
        return post.scalars().first()

    async def get_all_post(self):
        """Получить все объекты постов."""
        all_post = await self.session.execute(select(Posts))
        return all_post.scalars().all()

    async def create_post(
        self,
        post_data: PostsCreateAndUpdateRequest,
        user_id: UUID
    ) -> Posts:
        """Создать новый пост."""
        post_data = post_data.dict()
        post_data["user_id"] = user_id
        new_post = Posts(**post_data)

        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)
        return new_post

    async def update_post(
        self,
        post_id: UUID,
        post_data: PostsCreateAndUpdateRequest
    ) -> Posts:
        """Изменить объект поста."""
        post_data = post_data.dict()
        update_data = (
            update(
                Posts
            ).where(
                Posts.id == post_id
            ).values(**post_data)
        )
        await self.session.execute(update_data)
        await self.session.commit()
        return await self.get_post(post_id)

    async def delete_post(self, post_id: UUID) -> None:
        """Удалить объект поста"""
        delete_post = delete(Posts).where(Posts.id == post_id)
        await self.session.execute(delete_post)
        await self.session.commit()


async def get_posts_service(session: AsyncSession = Depends(get_session)) -> PostsService:
    return PostsService(session)
