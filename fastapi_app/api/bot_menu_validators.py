from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.bot_menu import bot_menu_crud, bot_menu_files_crud
from models.bot_menu import MenuButton, MenuButtonFile
from services.files import file_exists


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


async def check_button_file_exist(
    file_id: int, session: AsyncSession
) -> MenuButtonFile:
    file = await bot_menu_files_crud.get(file_id, session)
    if not file:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Файл с id {file_id} не существует.',
        )
    return file


async def check_button_image_file_exist(
    button_id: int, session: AsyncSession
) -> str:
    button = await check_button_exist(button_id, session)
    if not button.content_image:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Файл не назначен, для данной кнопки.',
        )
    if not file_exists(button.content_image):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Файл не найден на сервере.',
        )
    return button.content_image
