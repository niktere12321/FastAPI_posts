from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic.schema import UUID

from app.api.response_models.dislikes import DislikesResponse
from app.core.db.models import User
from app.core.db.user import current_user
from app.crud.dislikes_crud import DislikesService, get_dislikes_service


STR_POST_ENTITY_NOT_EXIST = "Поста с таким ID не существует"
STR_LIKE_ENTITY_NOT_EXIST = "Дизлайка с таким ID не существует"
STR_FORBIDDEN = "Нету прав для создания дизлайка"

router = APIRouter()


@router.post(
    "/{post_id}",
    response_model=DislikesResponse,
    response_model_exclude_none=True,
    summary="Создать новый дизлайк.",
    response_description="Полная информация о новом дизлайке.",
    dependencies=[Depends(current_user)],
)
async def create_dislike(
    post_id: UUID,
    user: User = Depends(current_user),
    dislikes_service: DislikesService = Depends(get_dislikes_service)
):
    """Создать дизлайк."""
    post = await dislikes_service.get_post_to_check(post_id)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_POST_ENTITY_NOT_EXIST)
    if post.user_id == user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    like = await dislikes_service.get_like_to_check(post_id, user.id)
    if like is not None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    dislike = await dislikes_service.get_dislike(post_id, user.id)
    if dislike is not None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    new_dislike = await dislikes_service.create_dislike(post_id, user.id)
    return new_dislike


@router.delete(
    "/{dislike_id}",
    summary="Удалить дизлайк к посту.",
    response_description="ID удаленного дизлайка.",
    dependencies=[Depends(current_user)],
)
async def delete_dislike(
    dislike_id: UUID,
    user: User = Depends(current_user),
    dislikes_service: DislikesService = Depends(get_dislikes_service)
):
    """Удалить дизлайк."""
    dislike = await dislikes_service.get_dislike_by_id(dislike_id)
    if dislike is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_LIKE_ENTITY_NOT_EXIST)
    if dislike.user_id != user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    await dislikes_service.delete_dislike(dislike_id)
    return dislike_id
