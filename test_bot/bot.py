import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from aiogram import Router
# from aiogram.utils import Token
from aiogram import types

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Вставьте сюда свой токен бота
# TOKEN = os.getenv('TOKEN')
TOKEN = 

# Создание экземпляра бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создание маршрутизатора
router = Router()

# Хендлер для команды /start


@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Проверка связи!!!")

# Хендлер для любого текстового сообщения


@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# Регистрация роутера
dp.include_router(router)

# Запуск бота


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
