import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings
from routers import admin, main_menu, managers, navigation, tree_commands
from utils.menus import set_commands

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    if not settings.app.token:
        raise ValueError(
            "Не найден токен бота. Пожалуйста,"
            "добавьте BOT_CONFIG__APP__TOKEN в .env файл."
        )
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(
        token=settings.app.token
    )
    await set_commands(bot)
    dp.include_router(main_menu.router)
    dp.include_router(navigation.router)
    dp.include_router(tree_commands.router)
    dp.include_router(admin.router)
    dp.include_router(managers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())