from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from models.contact_requests import ContactRequest
from models.user import User
from schemas.contact_requests import ContactRequestCreate, ContactRequestUpdate


class CRUDContactRequests(
    CRUDBase[ContactRequest, ContactRequestCreate, ContactRequestUpdate]
):
    def __init__(self) -> None:
        super().__init__(ContactRequest)

    async def get_all_not_processed(
        self, session: AsyncSession
    ) -> list[ContactRequest]:
        return await self._get_by_attribute('is_processed', False, session)

    async def get_all_processed(
        self, session: AsyncSession
    ) -> list[ContactRequest]:
        return await self._get_by_attribute('is_processed', True, session)

    async def get_contact_request_with_manager(
        self, contact_request_id: int, session: AsyncSession
    ) -> ContactRequest:
        contact_request = await session.execute(
            select(ContactRequest)
            .where(ContactRequest.id == contact_request_id)
            .options(selectinload(ContactRequest.manager))
        )
        return contact_request.scalars().first()

    async def take_to_work(
        self,
        contact_request: ContactRequest,
        manager: User,
        session: AsyncSession,
    ) -> ContactRequest:
        contact_request.in_progress = True
        contact_request.manager = manager
        await self._commit_and_refresh(contact_request, session)
        return await self.get_contact_request_with_manager(
            contact_request.id, session
        )


contact_requests_crud = CRUDContactRequests()
