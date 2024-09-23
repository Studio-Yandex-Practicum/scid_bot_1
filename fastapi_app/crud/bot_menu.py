from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.bot_menu import MenuButton
from schemas.bot_menu import MenuButtonCreate, MenuButtonUpdate


class CRUDBotMenu(CRUDBase[MenuButton, MenuButtonCreate, MenuButtonUpdate]):
    def __init__(self) -> None:
        super().__init__(MenuButton)

    async def get_children_button(
        self, button_id: int, session: AsyncSession
    ) -> list[MenuButton]:
        result = await session.execute(
            select(MenuButton).where(MenuButton.parent_id == button_id)
        )
        return result.scalars().all()


bot_menu_crud = CRUDBotMenu()
