from aiogram import Router

from .handlers import router as actions_kb_callback_router

# Cоздание маршрутизатора
# __name__ - для идентификации в логировании
router = Router(name=__name__)

router.include_routers(
    actions_kb_callback_router,
)
