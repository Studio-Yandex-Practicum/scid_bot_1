import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# from routers import tree_commands
from core.config import settings
from routers import main_menu, navigation
from handlers import main_button



async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    dp = Dispatcher(storage=MemoryStorage())

    bot = Bot(token=settings.app.token)

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
    # dp.include_router(tree_commands.router) # подключаем роутер с деревом

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())