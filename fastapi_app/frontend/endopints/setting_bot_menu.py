from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import check_user_is_superuser
from core.db import get_async_session
from core.frontend import templates
from crud.bot_menu import bot_menu_crud
from models.user import User


router = APIRouter(tags=['frontend_setting_bot_menu'])


@router.get(
    '/setting-bot-menu/list',
    response_class=HTMLResponse,
    summary='Список кнопок бота',
)
async def setting_bot_menu(
    request: Request,
    parent_sort: str = Query('asc'),
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session)
):
    buttons = await bot_menu_crud.get_all(session=session)
    buttons.sort(
        key=lambda button: 0 if button.parent_id is None else button.parent_id,
        reverse=False if parent_sort == 'asc' else True
    )
    context = {
        'request': request,
        'user': user,
        'buttons': buttons,
        'url_to_sort': request.url_for(
            'setting_bot_menu'
        ).include_query_params(
            parent_sort='desc' if parent_sort == 'asc' else 'asc'
        )
    }
    
    return templates.TemplateResponse(
        'setting_bot_menu/bot_menu_list.html', context
    )


@router.get(
    '/setting-bot-menu/add-button',
    response_class=HTMLResponse,
    summary='Создание кнопки бота',
)
async def setting_bot_menu(
    request: Request,
    parent_sort: str = Query('asc'),
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session)
):
    buttons = await bot_menu_crud.get_all(session=session)
    buttons.sort(
        key=lambda button: 0 if button.parent_id is None else button.parent_id,
        reverse=False if parent_sort == 'asc' else True
    )
    context = {
        'request': request,
        'user': user,
        'buttons': buttons,
        'url_to_sort': request.url_for(
            'setting_bot_menu'
        ).include_query_params(
            parent_sort='desc' if parent_sort == 'asc' else 'asc'
        )
    }
    
    return templates.TemplateResponse(
        'setting_bot_menu/bot_menu_create_update.html', context
    )
