import os
import aiohttp
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from aiogram import Router, types

load_dotenv()


logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN environment variable is not set!")
API_URL = os.getenv('API_URL')
if not API_URL:
    raise ValueError("API_URL environment variable is not set!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


router = Router()


@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Проверка связи!!!")

# Проверка API
@dp.message_handler(Command('api'))
async def call_api(message: Message):
    await message.answer("Обращаюсь к FastAPI...")

    # Выполняем запрос к эндпоинту FastAPI
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/api") as response:
                if response.status == 200:
                    data = await response.json()  # Парсим JSON-ответ
                    # Отправляем результат пользователю
                    await message.answer(f"Ответ от FastAPI: {data}")
                else:
                    # Если ответ не OK
                    await message.answer(f"Ошибка при обращении к FastAPI: статус {response.status}")
        except Exception as e:
            # В случае ошибки выводим сообщение об ошибке
            await message.answer(f"Произошла ошибка при обращении к FastAPI: {str(e)}")


@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
