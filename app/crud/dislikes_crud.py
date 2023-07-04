from fastapi import Depends
from pydantic.schema import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_session
from app.core.db.models import Likes, Posts, Dislikes


class DislikesService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_post_to_check(
        self,
        post_id: UUID,
    ) -> Posts:
        """Получить объект поста для проверки"""
        post = await self.session.execute(
            select(Posts).where(Posts.id == post_id)
        )
        return post.scalars().first()

    async def get_like_to_check(
        self,
        post_id: UUID,
        user_id: UUID
    ) -> Likes:
        """Получить объект лайка для проверки"""
        like = await self.session.execute(
            select(Likes).where(Likes.post_id == post_id).where(Likes.user_id == user_id)
        )
        return like.scalars().first()

    async def get_dislike(
        self,
        post_id: UUID,
        user_id: UUID
    ) -> Dislikes:
        """Получить объект лайка по id поста и пользователя."""
        dislike = await self.session.execute(
            select(Dislikes).where(Dislikes.post_id == post_id).where(Dislikes.user_id == user_id)
        )
        return dislike.scalars().first()

    async def get_dislike_by_id(
        self,
        dislike_id: UUID
    ) -> Dislikes:
        """Получить объект лайка по id."""
        dislike = await self.session.execute(
            select(Dislikes).where(Dislikes.id == dislike_id)
        )
        return dislike.scalars().first()

    async def create_dislike(
        self,
        post_id: UUID,
        user_id: UUID
    ) -> Dislikes:
        """Создать новый лайк"""
        new_dislike = Dislikes(post_id=post_id, user_id=user_id)

        self.session.add(new_dislike)
        await self.session.commit()
        await self.session.refresh(new_dislike)
        return new_dislike

    async def delete_dislike(self, dislike_id: UUID) -> None:
        delete_dislike = delete(Dislikes).where(Dislikes.id == dislike_id)
        await self.session.execute(delete_dislike)
        await self.session.commit()


async def get_dislikes_service(session: AsyncSession = Depends(get_session)) -> DislikesService:
    return DislikesService(session)
