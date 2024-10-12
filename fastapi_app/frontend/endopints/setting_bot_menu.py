from typing import Optional
from urllib.parse import quote

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.bot_menu_validators import check_button_exist
from api.dependencies.auth import check_user_is_superuser
from api.endpoints.bot_menu import delete_bot_menu_button_file, delete_bot_menu_button, update_bot_menu_button
from core.config import settings
from core.db import get_async_session
from core.frontend import templates
from crud.bot_menu import bot_menu_crud, bot_menu_files_crud
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
    session: AsyncSession = Depends(get_async_session),
):
    buttons = await bot_menu_crud.get_all(session=session)
    buttons.sort(
        key=lambda button: 0 if button.parent_id is None else button.parent_id,
        reverse=False if parent_sort == 'asc' else True,
    )
    context = {
        'request': request,
        'user': user,
        'buttons': buttons,
        'url_to_sort': request.url_for(
            'setting_bot_menu'
        ).include_query_params(
            parent_sort='desc' if parent_sort == 'asc' else 'asc'
        ),
    }

    return templates.TemplateResponse(
        'setting_bot_menu/bot_menu_list.html', context
    )


@router.get(
    '/setting-bot-menu/add-button/{parent_id}',
    response_class=HTMLResponse,
    summary='Создание кнопки бота',
)
async def setting_bot_menu_add_button(
    request: Request,
    parent_id: int,
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    context = {
        'request': request,
        'user': user,
        'buttons': '',
        'url_to_sort': '',
    }

    return templates.TemplateResponse(
        'setting_bot_menu/bot_menu_create_update.html', context
    )


@router.get(
    '/setting-bot-menu/update-button/{button_id}',
    response_class=HTMLResponse,
    summary='Страница обновления кнопки бота',
)
async def setting_bot_menu_update_button(
    request: Request,
    button_id: int,
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        button = await check_button_exist(button_id=button_id, session=session)
    except HTTPException:
        raise HTTPException(
            headers={
                'location': f'/?navbar_error={
                    quote(
                        'Такой кнопки не существует'
                    )
                }'
            },
            status_code=status.HTTP_302_FOUND,
        )
    context = {
        'request': request,
        'user': user,
        'button': button,
        'child_buttons': await bot_menu_crud.get_children_button(
            button_id=button_id, session=session
        ),
        'button_files': await bot_menu_files_crud.get_all_files_info(
            button_id=button_id, session=session
        ),
        'files_folder': str(settings.app.base_dir_for_files),
        'update': True,
    }

    return templates.TemplateResponse(
        'setting_bot_menu/bot_menu_create_update.html', context
    )


@router.get(
    '/setting-bot-menu/get-attach-file/{file_id}',
    response_class=HTMLResponse,
    summary='Получить прикрепленный файл',
    dependencies=[Depends(check_user_is_superuser)]
)
async def setting_bot_menu_get_attach_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    file = await bot_menu_files_crud.get(obj_id=file_id, session=session)
    return FileResponse(
        path=file.file_path,
        filename=file.file_path,
        media_type='multipart/form-data'
    )


@router.delete(
    '/setting-bot-menu/delete-attach-file/{button_id}/{file_id}',
    response_class=HTMLResponse,
    summary='Удалить прикреплённый файл',
    dependencies=[Depends(check_user_is_superuser)]
)
async def setting_bot_menu_delete_attach_file(
    file_id: int,
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await delete_bot_menu_button_file(
        button_id=button_id,
        file_id=file_id,
        session=session
    )


@router.delete(
    '/setting-bot-menu/delete-button/{button_id}',
    response_class=HTMLResponse,
    summary='Удалить прикреплённый файл',
)
async def setting_bot_menu_delete_button(
    request: Request,
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(check_user_is_superuser)
):
    await delete_bot_menu_button(
        button_id=button_id,
        session=session
    )
    return JSONResponse(
        content={ 'url': str(request.url_for('setting_bot_menu')) }
    )


@router.post(
    '/setting-bot-menu/update-button/{button_id}',
    response_class=HTMLResponse,
    summary='Обновление кнопки',
)
async def start_setting_bot_menu_update_button(
    request: Request,
    button_id: int,
    label: str = Form(None),
    content_text: Optional[str] = Form(None),
    content_image: Optional[UploadFile] = File(None),
    content_link: Optional[str] = Form(None),
    remove_content_image: bool = Form(False),
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    if not content_image.filename:
        content_image = None
    button = await update_bot_menu_button(
        button_id=button_id,
        label=label,
        content_image=content_image,
        content_link=content_link,
        content_text=content_text,
        remove_content_image=remove_content_image,
        session=session,
    )
    return await setting_bot_menu_update_button(
        request=request,
        button_id=button.id,
        session=session
    )
