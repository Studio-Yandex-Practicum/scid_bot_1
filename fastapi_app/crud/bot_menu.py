from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.bot_menu import MenuButton
from schemas.bot_menu import MenuButtonCreate, MenuButtonUpdate


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
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_children_button(
        self, button_id: int, session: AsyncSession
    ) -> list[MenuButton]:
        result = await session.execute(
            select(MenuButton).where(MenuButton.parent_id == button_id)
        )
        return result.scalars().all()


bot_menu_crud = CRUDBotMenu()
