from urllib.parse import quote

from fastapi import Depends, HTTPException, Request, status
from pydantic import ValidationError

from core.users import get_jwt_strategy, get_user_manager
from models.user import User


async def get_user_token(request: Request) -> str | None:
    token = request.cookies.get('Authorization')
    if token:
        return token.split(' ')[1] if ' ' in token else token


async def check_conditions_with_error(
    conditions: bool,
    location: str,
    error_text: str
) -> User:
    if not conditions:
        raise HTTPException(
                headers={
                    'location': f'{location}?error={
                        quote(error_text)
                    }'
                },
                status_code=status.HTTP_302_FOUND,
            )


async def verify_jwt_token(
    request: Request, user_manager=Depends(get_user_manager)
) -> User:
    token = await get_user_token(request)
    if token:
        try:
            jwt_strategy = get_jwt_strategy()
            user = await jwt_strategy.read_token(token, user_manager)
            await check_conditions_with_error(
                conditions=user is not None or user.is_active,
                location='/login',
                error_text='Неверные данные или истекло время авторизации'
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


async def check_user_is_superuser(
    request: Request,
    user_manager=Depends(get_user_manager)
) -> User:
    user = await verify_jwt_token(request, user_manager)
    await check_conditions_with_error(
        conditions=user.is_superuser,
        location='/login',
        error_text='Страница доступна только администратору'
    )
    return user


async def check_user_is_manager_or_superuser(
    request: Request,
    user_manager=Depends(get_user_manager)
) -> User:
    user = await verify_jwt_token(request, user_manager)
    await check_conditions_with_error(
        conditions=user.is_superuser or user.is_manager,
        location='/login',
        error_text='Страница доступна только администратору или менеджеру'
    )
    return user