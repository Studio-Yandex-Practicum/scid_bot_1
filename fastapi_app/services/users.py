import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from core.db import get_async_session
from core.users import current_user, get_user_db, get_user_manager
from schemas.users import UserCreate, UserPasswordUpdate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str,
    name: str,
    password: str,
    telegram_user_id: str = None,
    is_superuser: bool = False,
    is_manager: bool = False
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            name=name,
                            password=password,
                            telegram_user_id=telegram_user_id,
                            is_superuser=is_superuser,
                            is_manager=is_manager
                        )
                    )
                    print(f'Пользователь создан: {user.email}')
    except UserAlreadyExists:
        print(f'Пользователь {email} уже существует')
