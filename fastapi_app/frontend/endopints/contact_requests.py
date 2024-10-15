from urllib.parse import quote

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import (
    check_user_is_superuser,
    check_user_is_manager_or_superuser
)
from api.contact_requests_validators import check_contact_request_exist
from api.endpoints.contact_requests import (
    close_contact_request,
    delete_contact_request,
    take_contact_request_to_work
)
from core.db import get_async_session
from core.frontend import templates
from crud.contact_requests import contact_requests_crud

from models.contact_requests import ContactRequest
from models.user import User
from services.frontend import redirect_by_httpexeption

router = APIRouter(
    tags=['frontend_contact_requests'],
    prefix='/fr_contact_requests'
)


@router.get(
    '/list/{contact_request_type}',
    response_class=HTMLResponse,
    summary='Список заявок на обратную связь',
)
async def contact_requests_main(
    request: Request,
    contact_request_type: str,
    user: User = Depends(check_user_is_manager_or_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    managers = await contact_requests_crud.get_all(
        user=user,
        session=session,
        for_current_user=(
            not user.is_superuser and
            contact_request_type != 'new'
        ),
        in_progress=(
            contact_request_type == 'work' or
            contact_request_type == 'processed'
        ),
        is_processed=contact_request_type == 'processed'
    )
    managers.sort(
        key=lambda manager: manager.created_at,
    )
    context = {
        'request': request,
        'user': user,
        'contact_requests': managers,
        'contact_request_type': contact_request_type
    }
    return templates.TemplateResponse(
        'contact_requests/contact_requests_list.html',
        context
    )


@router.get(
    '/{contact_request_id}/{contact_request_type}',
    response_class=HTMLResponse,
    summary='Страница информации о заявке',
)
async def contact_request_details(
    request: Request,
    contact_request_id: int,
    contact_request_type: str,
    user: User = Depends(check_user_is_manager_or_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        contact_request = await check_contact_request_exist(
            contact_request_id=contact_request_id, session=session
        )
    except HTTPException:
        await redirect_by_httpexeption(
            location=f'/?navbar_error={quote(
                'Заявки на обратную связь не существует'
            )}'
        )
    print(contact_request.id)
    context = {
        'request': request,
        'user': user,
        'contact_request': contact_request,
        'contact_request_type': contact_request_type
    }
    return templates.TemplateResponse(
        'contact_requests/contact_request_details.html', context
    )


@router.post(
    '/close/{contact_request_id}',
    response_class=HTMLResponse,
    summary='Метод принятия заявки в работу',
    dependencies=[Depends(check_user_is_manager_or_superuser)]
)
async def contact_request_close(
    request: Request,
    contact_request_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    print(contact_request_id)
    await close_contact_request(
        contact_request_id=contact_request_id,
        session=session
    )
    return JSONResponse(
        content={ 
            'url': str(request.url_for(
                'contact_requests_main',
                contact_request_type='work'
                )
            ) 
        }
    )


@router.post(
    '/to-work/{contact_request_id}',
    response_class=HTMLResponse,
    summary='Метод принятия заявки в работу',
    dependencies=[Depends(check_user_is_manager_or_superuser)]
)
async def contact_request_to_work(
    request: Request,
    contact_request_id: int,
    user: User = Depends(check_user_is_manager_or_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    print(contact_request_id)
    await take_contact_request_to_work(
        contact_request_id=contact_request_id,
        managet_telegram_id=user.telegram_user_id,
        session=session
    )
    return JSONResponse(
        content={ 
            'url': str(request.url_for(
                'contact_request_details',
                contact_request_id=contact_request_id,
                contact_request_type='work'
                )
            ) 
        }
    )


@router.delete(
    '/{contact_request_id}/{contact_request_type}',
    response_class=HTMLResponse,
    summary='Удалить менеджера',
    dependencies=[Depends(check_user_is_superuser)]
)
async def contact_request_delete(
    request: Request,
    contact_request_id: int,
    contact_request_type: str,
    session: AsyncSession = Depends(get_async_session),
):
    await delete_contact_request(
        request_id=contact_request_id,
        session=session
    )
    return JSONResponse(
        content={ 
            'url': str(request.url_for(
                'contact_requests_main',
                contact_request_type=contact_request_type
                )
            ) 
        }
    )