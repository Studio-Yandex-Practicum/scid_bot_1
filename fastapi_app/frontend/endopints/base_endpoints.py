from typing import Optional
from urllib.parse import quote

import httpx
from fastapi import APIRouter, Depends, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi_users.password import PasswordHelper

from api.dependencies.auth import get_user_token, verify_jwt_token
from core.config import settings
from core.users import get_jwt_strategy, get_user_manager, current_user
from models.user import User
from services.email import send_change_password_email

router = APIRouter(tags=['frontend'])
templates = Jinja2Templates(directory='static/templates')


@router.post(
    '/logout_user',
    response_class=HTMLResponse,
    summary='Выход пользователя из системы'
)
async def logout_user(
    request: Request,
):
    response = RedirectResponse(
        request.url_for('main_page'),
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.delete_cookie(key='Authorization', httponly=True, secure=True)
    return response


async def change_user_password(
    request: Request,
    new_password: str,
):
    url = str(request.url_for('users:patch_current_user'))
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {await get_user_token(request)}",
        "Content-Type": "application/json"
    }
    data = {
        "password": new_password
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=data, headers=headers)
    if response.status_code != 200:
        return RedirectResponse(
            request.url_for('change_password', error=quote(
                    'Что-то пошло не так'
                )
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get(
    '/login',
    response_class=HTMLResponse,
    name='login_page',
    summary='Страница входа в админку'
)
async def login_page(request: Request, error: Optional[str] = None):
    context = {'request': request, 'error': error}
    return templates.TemplateResponse('login.html', context)


@router.get(
    '/forgot-password',
    response_class=HTMLResponse,
    summary='Страница сброса пароля'
)
async def forgot_password(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('forgot_password.html', context)


@router.post(
    '/forgot-password',
    response_class=HTMLResponse,
    summary='запуск механизма сброса пароля'
)
async def start_forgot_password(
    request: Request,
    email: str = Form(...),
    user_manager = Depends(get_user_manager)
):
    user = await user_manager.get_by_email(email)
    if user:
        await user_manager.forgot_password(user, request)
    return RedirectResponse(
        request.url_for('login_page'),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    '/change-password',
    response_class=HTMLResponse,
    summary='Страница смены пароля',
    name='change_password',
    dependencies=[Depends(verify_jwt_token)]
)
async def change_password(
    request: Request,
    error: Optional[str] = None
):
    context = {'request': request, 'error': error}
    return templates.TemplateResponse('change_password.html', context)


@router.post(
    '/change-password',
    response_class=HTMLResponse,
    summary='Запуск механизма смены пароля'
)
async def start_change_password(
    request: Request,
    old_password: str = Form(...),
    new_password1: str = Form(...),
    new_password2: str = Form(...),
    user: User = Depends(verify_jwt_token),
    user_manager = Depends(get_user_manager)
):
    if new_password1 != new_password2:
        raise HTTPException(
            headers={
                'location': f'/change-password?error={
                    quote(
                        "Новые пароли не совпадают"
                    )
                }'
            },
            status_code=status.HTTP_302_FOUND,
        )
    password_helper = PasswordHelper()
    verify_password, m = password_helper.verify_and_update(
        plain_password=old_password,
        hashed_password=user.hashed_password
    )
    if not verify_password:
        raise HTTPException(
            headers={
                'location': f'/change-password?error={
                    quote(
                        "Старый пароль указан неверно"
                    )
                }'
            },
            status_code=status.HTTP_302_FOUND,
        )
    await change_user_password(
        request,
        new_password1
    )
    await send_change_password_email(
        user.email,
        new_password1,
        'mail_change_password.html'
    )
    return RedirectResponse(
            request.url_for('login_page'),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get(
    '/',
    response_class=HTMLResponse,
    summary='Загрузка главной страницы',
)
async def main_page(request: Request, user: User = Depends(verify_jwt_token)):
    context = {'request': request, 'user': user}
    return templates.TemplateResponse('index.html', context)


@router.post(
    '/authorization',
    response_class=HTMLResponse,
    summary='Промежуточная страница авторизации и получения токена'
)
async def authorization(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user_manager=Depends(get_user_manager),
):
    user = await user_manager.authenticate(
        OAuth2PasswordRequestForm(
            grant_type='password', username=username, password=password
        )
    )
    if user is None:
        raise HTTPException(
            headers={
                'location': f'/login?error={
                    quote("Пользователь не найден")
                }'
            },
            status_code=status.HTTP_302_FOUND,
        )
    jwt_strategy = get_jwt_strategy()
    access_token = await jwt_strategy.write_token(user)
    response = RedirectResponse(
        request.url_for('main_page'),
        headers={'Authorization': f'Bearer {access_token}'},
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='Authorization',
        value=f'Bearer {access_token}',
        max_age=settings.security.jwt_lifetime,
        httponly=True,
        secure=True,
    )
    return response
