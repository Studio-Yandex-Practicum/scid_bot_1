from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.contact_requests import contact_requests_crud
from models.contact_requests import ContactRequest


async def check_contact_request_exist(
    contact_request_id: int,
    session: AsyncSession,
) -> Optional[ContactRequest]:
    return await check_object_exist(
        contact_request_id,
        contact_requests_crud,
        f'Запроса на обратную связь с id {contact_request_id} не существует.',
        session,
    )


async def check_contact_request_is_not_to_work(
    contact_request_id: int,
    session: AsyncSession,
) -> Optional[ContactRequest]:
    contact_request = await check_contact_request_exist(
        contact_request_id=contact_request_id, session=session
    )
    if contact_request.in_progress:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Заявка на обратную связь с id {contact_request_id} '
                f'уже в работе.'
            ),
        )
    return contact_request
