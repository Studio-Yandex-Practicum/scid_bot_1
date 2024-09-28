import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from core.db import get_async_session
from core.users import get_user_db, get_user_manager, current_user
from schemas.users import UserCreate, UserPasswordUpdate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
                    print(f'Пользователь создан: {user}')
    except UserAlreadyExists:
        print(f'Пользователь {email} уже существует')
