from crud.base import CRUDBase
from models.contact_requests import ContactRequest
from models.user import User
from schemas.users import UserCreate, UserUpdate
from sqlalchemy import select
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

    async def get_all_managers(self, session: AsyncSession) -> User:
        managers = await session.execute(
            select(User).where(
                User.is_manager == True,
                User.is_superuser == False
            )
        )
        return managers.scalars().all()

    async def delete_user(self, user: User, session: AsyncSession) -> User:
        contact_requests = await session.execute(
            select(ContactRequest).where(ContactRequest.manager_id == user.id)
        )
        contact_requests = contact_requests.scalars().all()
        for contact_request in contact_requests:
            if contact_request.is_processed == False:
                contact_request.in_progress = False
            contact_request.manager = None
        await session.delete(user)
        await session.commit()


user_crud = CRUDUser()
