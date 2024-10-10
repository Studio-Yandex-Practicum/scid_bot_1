# ограничение на import, будет импортирован только router
__all__ = ("router",)

from aiogram import Router

from .callback_handlers import router as callback_router
from .commands import router as commands_router

# Cоздание главного маршрутизатора
# __name__ - для идентификации в логировании
router = Router(name=__name__)

# Подключаем в главный маршрутизатор остальные
router.include_routers(
    callback_router,
    commands_router,
)
