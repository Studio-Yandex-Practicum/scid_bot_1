from crud.base import CRUDBase
from models.user import User
from schemas.users import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDUser(CRUDBase[User, UserUpdate, UserCreate]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_user_by_tg_id(
        self, user_tg_id: str, session: AsyncSession
    ) -> User:
        return await self._get_first_by_attribute(
            "telegram_user_id", user_tg_id, session
        )


user_crud = CRUDUser()
