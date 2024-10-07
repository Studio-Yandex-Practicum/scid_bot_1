# Регистрация хендлеров
import asyncio
import logging

# aiogram - асинхронная библиотека для Telegram API
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

from config import bot_token
from routers import router as main_router


async def main():
    # Создаем диспатчер. Он управляет всеми входящими сообщениями и командами.
    # Отвечает за маршрутизацию событий от Telegram к обработчикам в боте.
    dp = Dispatcher()
    # Объявляем маршрутизатор. Управляет как определнные команды или типы
    # сообщений будут обрабатываться. Для структурированно обработки.
    dp.include_router(main_router)

    # Подключаем логирование
    logging.basicConfig(level=logging.INFO)

    # Создаем бота
    bot = Bot(
        token=bot_token,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    # Включаем поллинг. Пингуем сервера Telegram на входящие сообщения
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
