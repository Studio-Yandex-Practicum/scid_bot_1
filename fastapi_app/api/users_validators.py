from http import HTTPStatus
from typing import Optional

from api.base_validators import check_object_exist
from crud.user import user_crud
from fastapi import HTTPException
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def check_user_exist(
    user_id: int,
    session: AsyncSession,
) -> Optional[User]:
    return await check_object_exist(
        user_id,
        user_crud,
        f"Пользователтя с id {user_id} не существует.",
        session,
    )


async def check_user_exist_by_tg_id(
    user_telegram_id: int,
    session: AsyncSession,
) -> Optional[User]:
    user = await user_crud.get_user_by_tg_id(
        user_tg_id=user_telegram_id, session=session
    )
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=(f"Пользователя с ТГ-id {user_telegram_id} не существует."),
        )
    return user


async def check_user_is_manager(
    user_id: int,
    session: AsyncSession,
) -> Optional[User]:
    user = await check_user_exist(user_id=user_id, session=session)
    if not user.is_manager:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(f"Пользователя с id {user_id} не является менеджером."),
        )
    return user


async def check_user_is_not_superuser(user: User) -> Optional[User]:
    if user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(f'Пользователь {user.name} - это суперпользователь.'),
        )
    return user


async def check_email_not_use(
    user_email: int,
    session: AsyncSession,
) -> bool:
    user = await user_crud._get_first_by_attribute(
        attribute='email', value=user_email, session=session
    )
    if user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(f'Пользователя с email {user_email} уже существует.'),
        )
    return True
