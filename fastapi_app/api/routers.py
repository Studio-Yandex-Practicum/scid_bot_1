from fastapi import APIRouter

from .endpoints import bot_menu_router, user_router

main_router = APIRouter()
main_router.include_router(bot_menu_router)
main_router.include_router(user_router)
