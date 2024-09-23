from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.bot_menu import bot_menu_crud
from models.bot_menu import MenuButton
from schemas.bot_menu import MenuButtonCreateMainButton


async def check_main_menu_exist(session: AsyncSession):
    result = await session.execute(
        select(MenuButton).where(MenuButton.is_main_menu_button == True)
    )
    return result.scalars().first()


async def create_main_menu_button(session: AsyncSession):
    if await check_main_menu_exist(session) is None:
        await bot_menu_crud.create(
            obj_in=MenuButtonCreateMainButton(
                label='Главное меню',
                content_text=None,
                content_image=None,
                content_link=None,
                parent_id=None,
                is_main_menu_button=True,
            ),
            session=session,
        )
        print('Кнопка главного меню создана')
    else:
        print('Кнопка главного меню уже существует')
