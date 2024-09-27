from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.contact_requests_validators import check_contact_request_exist
from core.db import get_async_session
from core.users import current_superuser
from crud.contact_requests import contact_requests_crud
from models.contact_requests import ContactRequest
from schemas.contact_requests import (
    ContactRequestCreate,
    ContactRequestResponse,
    ContactRequestUpdate,
)

router = APIRouter(prefix='/contact_requests', tags=['contact_requests'])


@router.post(
    '/',
    response_model=ContactRequestResponse,
    summary='Создаёт заявку на обратную связь',
    description=('Заявка будет иметь статус "Не выполнена". Время UTC.'),
)
async def create_contact_request(
    contact_request: ContactRequestCreate,
    session: AsyncSession = Depends(get_async_session),
) -> ContactRequest:
    return await contact_requests_crud.create(
        obj_in=contact_request, session=session
    )


@router.get(
    '/all',
    response_model=list[ContactRequestResponse],
    dependencies=[Depends(current_superuser)],
    summary='Получает все заявки',
)
async def get_contact_request_with_is_processed_filter(
    is_processed: Optional[bool] = Query(
        None,
        description=(
            'None - все заявки, True - только выполненные заявки, '
            'False - только не выполненные заявки.'
        ),
    ),
    session: AsyncSession = Depends(get_async_session),
) -> list[ContactRequest]:
    if is_processed is None:
        return await contact_requests_crud.get_all(session=session)
    if is_processed == True:
        return await contact_requests_crud.get_all_processed(session=session)
    return await contact_requests_crud.get_all_not_processed(session=session)


@router.get(
    '/{request_id}',
    response_model=ContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary='Получает конкретную заявку',
)
async def get_contact_request(
    request_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> ContactRequest:
    return await check_contact_request_exist(
        contact_request_id=request_id,
        session=session,
    )


@router.patch(
    '/{request_id}',
    response_model=ContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary='Обновляет заявку',
    description=('Возможно обновить отметку о выполнении и способ связи.'),
)
async def update_contact_request(
    request_id: int,
    contact_request: ContactRequestUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await contact_requests_crud.update(
        db_obj=await check_contact_request_exist(
            contact_request_id=request_id,
            session=session,
        ),
        obj_in=contact_request,
        session=session,
    )


@router.delete(
    '/{request_id}',
    response_model=ContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет заявку',
)
async def delete_contact_request(
    request_id: int,
    session: AsyncSession = Depends(get_async_session),
):

    return await contact_requests_crud.delete(
        db_obj=await check_contact_request_exist(
            contact_request_id=request_id,
            session=session,
        ),
        session=session,
    )