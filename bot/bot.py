import asyncio
# import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import settings

from routers import (
    # main_menu,
    managers,
    # navigation,
    tree_commands,
    reviews
)
from routers.handlers import (base,
                              create_button,
                              get_button_content,
                              get_child_buttons,
                              putch_button_content,
                              putch_button_parent,
                              del_button_with_sub)

from utils.menus import set_commands
import os  #
from dotenv import load_dotenv  #


async def main():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    # )
    # if not settings.app.token:
    #     raise ValueError(
    #         "Не найден токен бота. Пожалуйста,"
    #         "добавьте BOT_CONFIG__APP__TOKEN в .env файл."
    #     )
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(
        token=settings.app.token
    )
    # load_dotenv()  #
    # # API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN2")  #
    # API_TOKEN = os.getenv("BOT_CONFIG__APP__TOKEN")  #
    # bot = Bot(token=API_TOKEN)  #

    await set_commands(bot)
    # dp.include_router(main_menu.router)
    # dp.include_router(navigation.router)
    dp.include_router(tree_commands.router)
    dp.include_router(managers.router)
    dp.include_router(reviews.router)  # роутер review
    dp.include_routers(
        base.router,
        create_button.router,
        get_button_content.router,
        get_child_buttons.router,
        del_button_with_sub.router,
        putch_button_parent.router,
        putch_button_content.router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
