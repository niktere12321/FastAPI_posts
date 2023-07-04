from typing import Union
import uuid

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, UUIDIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy, CookieTransport
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.db.db import get_session
from app.core.db.models import User
from app.api.request_models.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')
cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
cookie_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.uuid4]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 6:
            raise InvalidPasswordException(
                reason='Пароль должен быть больше 6 символов'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать адрес электронной почты'
            )


async def get_enabled_backends(request: Request):
    if request.url.path == "/protected-route-only-jwt":
        return [auth_backend]
    else:
        return [cookie_backend, auth_backend]


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.uuid4](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True, get_enabled_backends=get_enabled_backends)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
