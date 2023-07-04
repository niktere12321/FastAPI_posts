from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic.schema import UUID

from app.api.response_models.likes import LikesResponse
from app.core.db.models import User
from app.core.db.user import current_user
from app.crud.likes_crud import LikesService, get_likes_service


STR_POST_ENTITY_NOT_EXIST = "Поста с таким ID не существует"
STR_LIKE_ENTITY_NOT_EXIST = "Лайка с таким ID не существует"
STR_FORBIDDEN = "Нету прав для создания лайка"

router = APIRouter()


@router.post(
    "/{post_id}",
    response_model=LikesResponse,
    response_model_exclude_none=True,
    summary="Создать новый лайк.",
    response_description="Полная информация о новом лайке.",
    dependencies=[Depends(current_user)],
)
async def create_like(
    post_id: UUID,
    user: User = Depends(current_user),
    likes_service: LikesService = Depends(get_likes_service)
):
    """Создать лайк."""
    post = await likes_service.get_post_to_check(post_id)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_POST_ENTITY_NOT_EXIST)
    if post.user_id == user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    dislike = await likes_service.get_dislike_to_check(post_id, user.id)
    if dislike is not None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    like = await likes_service.get_like(post_id, user.id)
    if like is not None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    new_like = await likes_service.create_like(post_id, user.id)
    return new_like


@router.delete(
    "/{like_id}",
    summary="Удалить лайк к посту.",
    response_description="ID удаленного лайка.",
    dependencies=[Depends(current_user)],
)
async def delete_like(
    like_id: UUID,
    user: User = Depends(current_user),
    likes_service: LikesService = Depends(get_likes_service)
):
    """Удалить лайк."""
    like = await likes_service.get_like_by_id(like_id)
    if like is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_LIKE_ENTITY_NOT_EXIST)
    if like.user_id != user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    await likes_service.delete_like(like_id)
    return like_id
