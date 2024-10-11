from typing import Optional
from urllib.parse import quote

import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.password import PasswordHelper

from api.dependencies.auth import check_user_is_superuser
from core.config import settings
from core.frontend import templates
from core.users import current_superuser
from models.user import User
from services.email import send_change_password_email

router = APIRouter(tags=['frontend_setting_bot_menu'])


@router.get(
    '/setting-bot-menu',
    response_class=HTMLResponse,
    # dependencies=[Depends(current_superuser)],
    summary='Настройки контента бота',
)
async def setting_bot_menu(
    request: Request, user: User = Depends(check_user_is_superuser)
):
    context = {'request': request, 'user': user}
    return templates.TemplateResponse(
        'setting_bot_menu/bot_menu_list.html', context
    )
