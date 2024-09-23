from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.bot_menu import bot_menu_crud
from models.bot_menu import MenuButton


async def check_button_exist(
    button_id: int,
    session: AsyncSession,
) -> Optional[MenuButton]:
    button = await bot_menu_crud.get(obj_id=button_id, session=session)
    if button is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Кнопки с id {button_id} не существует.',
        )
    return button
