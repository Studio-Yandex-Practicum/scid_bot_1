import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.routers import tree_commands
from routers import main_menu, navigation
from handlers import main_button

load_dotenv()

TOKEN = os.getenv('TOKEN')


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())

    bot = Bot(token=TOKEN)

    # Andrey
    # Создаем бота
    #bot = Bot(
    #    token=TOKEN,
    #    session=AiohttpSession(),
    #    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    #)

    dp.include_router(main_menu.router)
    dp.include_router(navigation.router)

    # dp.include_router(main_button.router) # здесь подключаем хендлеры
    dp.include_router(tree_commands.router) # подключаем роутер с деревом

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())