from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.bot_menu import MenuButton, MenuButtonFile
from schemas.bot_menu import (
    MenuButtonCreate,
    MenuButtonFileCreate,
    MenuButtonFileUpdate,
    MenuButtonUpdate,
)


class CRUDBotMenu(CRUDBase[MenuButton, MenuButtonCreate, MenuButtonUpdate]):
    def __init__(self) -> None:
        super().__init__(MenuButton)

    async def create(
        self,
        parent_id: int,
        obj_in: MenuButtonCreate,
        session: AsyncSession,
    ) -> Optional[MenuButton]:
        obj_in_data = obj_in.model_dump()
        obj_in_data['parent_id'] = parent_id
        db_obj = self.model(**obj_in_data)
        return await self._commit_and_refresh(db_obj, session)

    async def get_main_menu_button(self, session: AsyncSession) -> MenuButton:
        result = await session.execute(
            select(MenuButton).where(MenuButton.is_main_menu_button == True)
        )
        return result.scalars().first()

    async def get_children_button(
        self, button_id: int, session: AsyncSession
    ) -> list[MenuButton]:
        result = await session.execute(
            select(MenuButton).where(MenuButton.parent_id == button_id)
        )
        return result.scalars().all()

    async def change_parent_button(
        self,
        menu_button: MenuButton,
        new_parent_id: int,
        session: AsyncSession,
    ) -> MenuButton:
        menu_button.parent_id = new_parent_id
        return await self._commit_and_refresh(menu_button, session)


class CRUDBotMenuFiles(
    CRUDBase[MenuButtonFile, MenuButtonFileCreate, MenuButtonFileUpdate]
):
    def __init__(self) -> None:
        super().__init__(MenuButtonFile)

    async def get_all_files_info(
        self, button_id: int, session: AsyncSession
    ) -> MenuButtonFile:
        result = await session.execute(
            select(MenuButtonFile).where(MenuButtonFile.button_id == button_id)
        )
        return result.scalars().all()


bot_menu_crud = CRUDBotMenu()
bot_menu_files_crud = CRUDBotMenuFiles()
