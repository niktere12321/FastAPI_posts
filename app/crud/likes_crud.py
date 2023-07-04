from fastapi import Depends
from pydantic.schema import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_session
from app.core.db.models import Likes, Posts, Dislikes


class LikesService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_post_to_check(
        self,
        post_id: UUID,
    ):
        """Получить объект поста для проверки"""
        post = await self.session.execute(
            select(Posts).where(Posts.id == post_id)
        )
        return post.scalars().first()

    async def get_dislike_to_check(
        self,
        post_id: UUID,
        user_id: UUID
    ) -> Dislikes:
        """Получить объект дизлайка для проверки"""
        dislike = await self.session.execute(
            select(Dislikes).where(Dislikes.post_id == post_id).where(Dislikes.user_id == user_id)
        )
        return dislike.scalars().first()

    async def get_like(
        self,
        post_id: UUID,
        user_id: UUID
    ) -> Likes:
        """Получить объект лайка по id поста и пользователя."""
        like = await self.session.execute(
            select(Likes).where(Likes.post_id == post_id).where(Likes.user_id == user_id)
        )
        return like.scalars().first()

    async def get_like_by_id(
        self,
        like_id: UUID
    ) -> Likes:
        """Получить объект лайка по id."""
        like = await self.session.execute(
            select(Likes).where(Likes.id == like_id)
        )
        return like.scalars().first()

    async def create_like(
        self,
        post_id: UUID,
        user_id: UUID
    ) -> Likes:
        """Создать новый лайк"""
        new_like = Likes(post_id=post_id, user_id=user_id)

        self.session.add(new_like)
        await self.session.commit()
        await self.session.refresh(new_like)
        return new_like

    async def delete_like(self, like_id: UUID) -> None:
        delete_like = delete(Likes).where(Likes.id == like_id)
        await self.session.execute(delete_like)
        await self.session.commit()


async def get_likes_service(session: AsyncSession = Depends(get_session)) -> LikesService:
    return LikesService(session)
