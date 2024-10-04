from urllib.parse import quote

from fastapi import Depends, Request, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from core.users import get_jwt_strategy, get_user_manager


async def get_user_token(request: Request) -> str | None:
    token = request.cookies.get('Authorization')
    if token:
        return token.split(' ')[1] if ' ' in token else token

async def verify_jwt_token(
    request: Request, user_manager=Depends(get_user_manager)
):
    token = await get_user_token(request)
    if token:
        try:
            jwt_strategy = get_jwt_strategy()
            user = await jwt_strategy.read_token(token, user_manager)
            if user is None or not user.is_active:
               raise HTTPException(
                    headers={
                        'location': f'/login?error={
                            quote(
                                "Неверные данные или истекло время авторизации"
                            )
                        }'
                    },
                    status_code=status.HTTP_302_FOUND,
                )
            return user
        except ValidationError:
            raise HTTPException(
                headers={
                    'location': f'/login?error={
                        quote(
                            "Неверные данные или истекло время авторизации"
                        )
                    }'
                },
                status_code=status.HTTP_302_FOUND,
            )
    raise HTTPException(
        headers={
            'location': f'/login?error={
                quote("Пользователь не авторизован")
            }'
        },
        status_code=status.HTTP_302_FOUND,
    )
