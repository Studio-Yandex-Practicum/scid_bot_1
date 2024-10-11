from core.users import auth_backend, get_user_manager
from fastapi.routing import APIRouter
from fastapi_users import FastAPIUsers
from models.user import User
from schemas.users import UserPasswordUpdate, UserRead

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
