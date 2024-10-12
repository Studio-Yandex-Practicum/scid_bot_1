from typing import Optional

from crud.base import CRUDBase
from models.contact_requests import ContactRequest
from models.user import User
from schemas.contact_requests import ContactRequestCreate, ContactRequestUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CRUDContactRequests(
    CRUDBase[ContactRequest, ContactRequestCreate, ContactRequestUpdate]
):
    def __init__(self) -> None:
        super().__init__(ContactRequest)

    async def _add_manager_id_and_options_to_query(
        self, attributes: dict[str, any], for_current_user: bool, user: User
    ) -> tuple[any, any]:
        if for_current_user:
            attributes.update({"manager_id": user.id})
        options = [selectinload(ContactRequest.manager)]
        return attributes, options

    async def get_all(
        self,
        session: AsyncSession,
        user: User,
        is_processed: Optional[bool] = None,
        in_progress: Optional[bool] = None,
        for_current_user: Optional[bool] = None,
    ) -> list[ContactRequest]:
        attributes = {}
        if is_processed is not None:
            attributes.update({"is_processed": is_processed})
        if in_progress is not None:
            attributes.update({"in_progress": in_progress})
        attributes, options = await self._add_manager_id_and_options_to_query(
            attributes, for_current_user, user
        )
        return await self._get_by_attributes(attributes, options, session)

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

    async def close_request(
        self, contact_request: ContactRequest, session: AsyncSession
    ) -> ContactRequest:
        contact_request.is_processed = True
        await self._commit_and_refresh(contact_request, session)
        return await self.get_contact_request_with_manager(
            contact_request.id, session
        )


contact_requests_crud = CRUDContactRequests()
