from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.bot_menu import bot_menu_crud, bot_menu_files_crud
from models.bot_menu import MenuButton, MenuButtonFile
from services.files import file_exists


async def check_button_exist(
    button_id: int,
    session: AsyncSession,
) -> Optional[MenuButton]:
    return await check_object_exist(
        button_id,
        bot_menu_crud,
        f'Кнопки с id {button_id} не существует.',
        session,
    )


async def check_button_file_exist(
    file_id: int, session: AsyncSession
) -> MenuButtonFile:
    return await check_object_exist(
        file_id,
        bot_menu_files_crud,
        f'Файл с id {file_id} не существует.',
        session,
    )


async def check_button_image_file_exist(
    button_id: int, session: AsyncSession
) -> str:
    button = await check_button_exist(button_id, session)
    if not button.content_image:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Файл не назначен, для данной кнопки.',
        )
    if not await file_exists(button.content_image):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Файл не найден на сервере.',
        )
    return button.content_image


async def check_button_is_main_menu_after_change_parent(
    button_id: int,
    session: AsyncSession
) -> MenuButton:
    button = await check_button_exist(button_id, session)
    if button.is_main_menu_button:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Нельзя именить родителя начальной кнопки.',
        )
    return button