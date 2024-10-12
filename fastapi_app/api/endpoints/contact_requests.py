from typing import Optional

from api.contact_requests_validators import (
    check_contact_request_exist,
    check_contact_request_is_not_to_work,
)

from api.dependencies.users import get_manager_or_superuser
from api.users_validators import check_user_exist_by_tg_id
from core.db import get_async_session
from core.users import current_superuser, current_user
from crud.contact_requests import contact_requests_crud
from fastapi import APIRouter, Depends, Query
from models.contact_requests import ContactRequest
from models.user import User
from schemas.contact_requests import (ContactRequestCreate,
                                      ContactRequestResponse,
                                      ContactRequestUpdate)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/contact_requests", tags=["contact_requests"])


@router.post(
    "{contact_request_id}/take-to-work",
    response_model=ContactRequestResponse,
    dependencies=[Depends(get_manager_or_superuser)],
    summary='Устанавливает статус заявки на "В работе", и указывает менеджера',
)
async def take_contact_request_to_work(
    contact_request_id: int,
    managet_telegram_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> ContactRequest:
    user = await check_user_exist_by_tg_id(
        user_telegram_id=managet_telegram_id, session=session
    )
    return await contact_requests_crud.take_to_work(
        contact_request=await check_contact_request_is_not_to_work(
            contact_request_id=contact_request_id, session=session
        ),
        manager=user,
        session=session,
    )


@router.post(
    '/close_request',
    response_model=ContactRequestResponse,
    summary='"Закрывает" заявку. Устанавливает статус выполнена.',
)
async def create_contact_request(
    contact_request_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> ContactRequest:
    return await contact_requests_crud.close_request(
        contact_request=await check_contact_request_exist(
            contact_request_id=contact_request_id, session=session
        ),
        session=session,
    )


@router.post(
    '/',
    response_model=ContactRequestResponse,
    summary="Создаёт заявку на обратную связь",
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
    "/all",
    response_model=list[ContactRequestResponse],
    dependencies=[Depends(get_manager_or_superuser)],
    summary="Получает все заявки",
)
async def get_contact_request_with_is_processed_filter(
    is_processed: Optional[bool] = Query(
        None,
        description=(
            "None - все заявки, True - только выполненные заявки, "
            "False - только не выполненные заявки."
        ),
    ),
    in_progress: Optional[bool] = Query(
        None,
        description=(
            "None - все заявки, True - только выполненные заявки, "
            "False - только не выполненные заявки."
        ),
    ),
    for_current_user: bool = Query(
        False,
        description=("Если True, то получает заявки текущего пользователя"),
    ),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[ContactRequest]:
    return await contact_requests_crud.get_all(
        is_processed=is_processed,
        in_progress=in_progress,
        for_current_user=for_current_user,
        user=user,
        session=session,
    )


@router.get(
    "/{request_id}",
    response_model=ContactRequestResponse,
    dependencies=[Depends(get_manager_or_superuser)],
    summary="Получает конкретную заявку",
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
    "/{request_id}",
    response_model=ContactRequestResponse,
    dependencies=[Depends(get_manager_or_superuser)],
    summary="Обновляет заявку",
    description=("Возможно обновить отметку о выполнении и способ связи."),
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
    "/{request_id}",
    response_model=ContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary="Удаляет заявку",
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
