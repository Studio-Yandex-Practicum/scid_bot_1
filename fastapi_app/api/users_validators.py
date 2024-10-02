from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.user import user_crud
from models.user import User


async def check_user_exist(
    user_id: int,
    session: AsyncSession,
) -> Optional[User]:
    return await check_object_exist(
        user_id,
        user_crud,
        f'Пользователтя с id {user_id} не существует.',
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
            detail=(f'Пользователя с ТГ-id {user_telegram_id} не существует.'),
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
            detail=(f'Пользователя с id {user_id} не является менеджером.'),
        )
    return user
