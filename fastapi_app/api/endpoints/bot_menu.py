from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.bot_menu_validators import check_button_exist
from core.db import get_async_session
from core.users import current_superuser
from crud.bot_menu import bot_menu_crud
from models.bot_menu import MenuButton
from schemas.bot_menu import (
    MenuButtonChildrenResponse,
    MenuButtonCreate,
    MenuButtonResponse,
    MenuButtonUpdate,
)

router = APIRouter(prefix='/bot_menu', tags=['bot_menu'])


@router.get(
    '/{button_id}/get-content',
    response_model=MenuButtonResponse,
    summary='Возвращает контент, который должна отображать кнопка',
    description=('Возвращает: текст, изображение, файлы, ссылку'),
)
async def get_button_content(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Optional[MenuButton]:
    return await check_button_exist(
        button_id=button_id,
        session=session,
    )


@router.get(
    '/{button_id}/get-child-buttons',
    response_model=list[MenuButtonChildrenResponse],
    summary='Возвращает список дочерних кнопок, для текущей',
    description=('Возвращает: id кнопки, родителя и её название'),
)
async def get_button_children(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[MenuButton]:
    await check_button_exist(
        button_id=button_id,
        session=session,
    )
    return await bot_menu_crud.get_children_button(
        button_id=button_id,
        session=session,
    )


@router.post(
    '/{button_id}/add-child-button',
    response_model=MenuButtonResponse,
    dependencies=[Depends(current_superuser)],
    summary='Добавляет кнопку в базу данных',
    description=('Добавляет кнопку к родителю, как дочернюю'),
)
async def create_new_bot_menu_button(
    button_id: int,
    bot_menu_button: MenuButtonCreate,
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    await check_button_exist(
        button_id=button_id,
        session=session,
    )
    return await bot_menu_crud.create(
        obj_in=bot_menu_button,
        parent_id=button_id,
        session=session,
    )
