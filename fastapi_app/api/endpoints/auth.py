from fastapi.routing import APIRouter
from fastapi_users import FastAPIUsers

from core.users import auth_backend, get_user_manager
from models.user import User
from schemas.users import UserCreate, UserRead, UserUpdate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(prefix='/auth')
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=['auth'],
)
