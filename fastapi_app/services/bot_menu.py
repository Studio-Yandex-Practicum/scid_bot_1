from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.bot_menu_validators import check_button_image_file_exist
from crud.bot_menu import bot_menu_crud
from models.bot_menu import MenuButton
from schemas.bot_menu import MenuButtonCreateMainButton
from services.files import delete_file, file_exists


async def check_main_menu_exist(session: AsyncSession):
    result = await session.execute(
        select(MenuButton).where(MenuButton.is_main_menu_button == True)
    )
    return result.scalars().first()


async def create_main_menu_button(session: AsyncSession):
    if await check_main_menu_exist(session) is None:
        await bot_menu_crud.create(
            parent_id=None,
            obj_in=MenuButtonCreateMainButton(
                label="Главное меню",
                content_text=None,
                content_image=None,
                content_link=None,
                parent_id=None,
                is_main_menu_button=True,
            ),
            session=session,
        )
        print("Кнопка главного меню создана")
    else:
        print("Кнопка главного меню уже существует")


async def delete_image_file_if_exist(button: MenuButton) -> str:
    if button.content_image is not None:
        await delete_file(button.content_image)
