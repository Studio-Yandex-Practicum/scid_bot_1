from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import get_async_session
from models.security import AccessToken
from models.user import User

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.security.secret,
        lifetime_seconds=settings.security.jwt_lifetime,
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield AccessToken(session, AccessToken)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.security.secret
    verification_token_secret = settings.security.secret

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
        ):
            print(f"User {user.id} has forgot their password. Reset token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_user = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_user.current_user(active=True)
current_superuser = fastapi_user.current_user(active=True, superuser=True)
