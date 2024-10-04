from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from api.dependencies.auth import verify_jwt_token
from core.config import settings
from core.users import get_jwt_strategy, get_user_manager
from models.user import User

router = APIRouter(tags=['frontend'])
templates = Jinja2Templates(directory='static/templates')


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
    '/',
    response_class=HTMLResponse,
    summary='Загрузка главной страницы',
)
async def main_page(request: Request, user: User = Depends(verify_jwt_token)):
    context = {'request': request, 'user': user}
    return templates.TemplateResponse('base.html', context)


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
