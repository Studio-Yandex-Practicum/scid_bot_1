from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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

router = APIRouter(prefix='/bot_menu')


@router.post(
    '/',
    response_model=MenuButtonResponse,
    dependencies=[Depends(current_superuser)],
)
async def create_new_bot_menu_button(
    bot_menu_button: MenuButtonCreate,
    session: AsyncSession = Depends(get_async_session),
) -> MenuButton:
    return await bot_menu_crud.create(
        obj_in=bot_menu_button,
        session=session,
    )
