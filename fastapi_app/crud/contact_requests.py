from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.contact_requests import ContactRequest
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


contact_requests_crud = CRUDContactRequests()
