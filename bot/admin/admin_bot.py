import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import (base,
                      create_button,
                      get_button_content,
                      get_child_buttons,
                      putch_button_content,
                      putch_button_parent,
                      del_button_with_sub)

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN2")
if not API_TOKEN:
    raise ValueError(
        "Не найден токен бота. Пожалуйста,"
        "добавьте TELEGRAM_BOT_TOKEN в .env файл."
    )

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=API_TOKEN)


async def main():
    # API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    dp = Dispatcher(storage=storage)

    dp.include_routers(
        base.router,
        create_button.router,
        get_button_content.router,
        get_child_buttons.router,
        del_button_with_sub.router,
        putch_button_parent.router,
        putch_button_content.router,
    )

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
