import json

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from api.users_validators import check_user_exist_by_tg_id
from core.db import get_async_session
from core.users import auth_backend, get_user_manager
from models.user import User
from schemas.users import UserPasswordUpdate, UserRead, UserJwtAndRoleRequest

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/jwt"
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)
users_routers = fastapi_users.get_users_router(UserRead, UserPasswordUpdate)
users_routers.routes = [
    route
    for route in users_routers.routes
    if route.name == "users:patch_current_user"
]
router.include_router(users_routers)


# Блин, все же ммне категорически не нравится получение токена, без логина и
# пароля... Не безопасно это.
@router.post(
    '/get_user-jwf-by-tg-id',
    response_model=UserJwtAndRoleRequest,
    summary=(
        'Получает jwt токен, в зависимости от привязанного tg-id, а так же '
        'привелегии пользователя'
    )
)
async def get_user_jwf_by_tg_id(
    tg_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[User]:
    user = await check_user_exist_by_tg_id(
        user_telegram_id=tg_id,
        session=session
    )
    response = await auth_backend.login(auth_backend.get_strategy(), user)
    jwt_dict = json.loads(response.body.decode('utf-8'))
    return UserJwtAndRoleRequest(
        jwt=jwt_dict['access_token'],
        token_type='Bearer',
        is_manager=user.is_manager,
        is_superuser=user.is_superuser
    )