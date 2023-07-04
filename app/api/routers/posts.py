from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic.schema import UUID

from app.api.request_models.posts import PostsCreateAndUpdateRequest
from app.api.response_models.posts import PostsResponse
from app.core.db.models import User
from app.core.db.user import current_user
from app.crud.posts_crud import PostsService, get_posts_service


STR_ENTITY_NOT_EXIST = "Поста с таким ID не существует"
STR_FORBIDDEN = "Нету прав для изменения поста"

router = APIRouter()


@router.get(
    "/",
    response_model=list[PostsResponse],
    response_model_exclude_none=True,
    summary="Получить информацию о всех постах.",
    response_description="Полная информация о всех постах.",
    dependencies=[Depends(current_user)],
)
async def get_all_posts(
    posts_service: PostsService = Depends(get_posts_service)
):
    """Информация о всех постах."""
    all_post = await posts_service.get_all_post()
    return all_post


@router.get(
    "/{post_id}",
    response_model=PostsResponse,
    response_model_exclude_none=True,
    summary="Получить информацию о посте.",
    response_description="Полная информация о посте.",
    dependencies=[Depends(current_user)],
)
async def get_post(
    post_id: UUID,
    posts_service: PostsService = Depends(get_posts_service)
):
    """Информация о посте."""
    post = await posts_service.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_ENTITY_NOT_EXIST)
    return post


@router.post(
    "/",
    response_model=PostsResponse,
    response_model_exclude_none=True,
    summary="Создать новый пост.",
    response_description="Полная информация о новом посте.",
    dependencies=[Depends(current_user)],
)
async def create_post(
    post_data: PostsCreateAndUpdateRequest,
    user: User = Depends(current_user),
    posts_service: PostsService = Depends(get_posts_service)
):
    """
    Создать пост.
      - **title** - название поста;
      - **description** - описание поста.
    """
    new_post = await posts_service.create_post(post_data, user.id)
    return new_post


@router.patch(
    "/{post_id}",
    response_model=PostsResponse,
    response_model_exclude_none=True,
    summary="Изменить пост.",
    response_description="Полная информация о посте.",
    dependencies=[Depends(current_user)],
)
async def update_post(
    post_id: UUID,
    post_data: PostsCreateAndUpdateRequest,
    user: User = Depends(current_user),
    posts_service: PostsService = Depends(get_posts_service)
):
    """Изменить пост.
    - **title**: название поста
    - **description**: описание поста
    """
    post = await posts_service.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_ENTITY_NOT_EXIST)
    if post.user_id != user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    post = await posts_service.update_post(post_id, post_data)
    return post


@router.delete(
    "/{post_id}",
    summary="Удалить пост.",
    response_description="ID удаленного поста.",
    dependencies=[Depends(current_user)],
)
async def delete_post(
    post_id: UUID,
    user: User = Depends(current_user),
    posts_service: PostsService = Depends(get_posts_service)
):
    """Удалить пост."""
    post = await posts_service.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=STR_ENTITY_NOT_EXIST)
    if post.user_id != user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=STR_FORBIDDEN)
    await posts_service.delete_post(post_id)
    return post_id
