from fastapi import APIRouter

from .endopints import frontend_base, frontend_bot_menu_router

frontend_router = APIRouter()
frontend_router.include_router(frontend_base)
frontend_router.include_router(frontend_bot_menu_router)