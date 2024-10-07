import os
from dotenv import load_dotenv
import logging
import aiohttp
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery)

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')

if not TOKEN or not API_URL:
    raise ValueError("Переменные окружения TOKEN или API_URL не установлены!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()


@router.message(Command("start"))
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Получить данные API", callback_data="call_api")]
        ]
    )
    await message.answer("Да работаю я, успокойся уже!", reply_markup=keyboard)

# test


@router.message(Command("test"))
async def send_content(message: Message):
    async with aiohttp.ClientSession() as session:
        # data = session.get(API_URL/)
        data = session.get(API_URL)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Получить данные API", callback_data="call_api")]
        ]
    )
    await message.answer("Да работаю я, успокойся уже!", reply_markup=keyboard)





# получить эндпоинты API
@router.callback_query(lambda c: c.data == 'call_api')
async def call_api_callback(callback: CallbackQuery):
    await callback.message.answer("Обращаюсь к FastAPI...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/openapi.json") as response:
                if response.status == 200:
                    data = await response.json()
                    paths = data.get('paths', {})
                    if paths:
                        api_info = "\n".join([f"{method.upper()} {path}" for path, methods in paths.items(
                        ) for method in methods.keys()])
                        await callback.message.answer(
                            f"Доступные эндпоинты FastAPI:\n{api_info}"
                        )
                    else:
                        await callback.message.answer(
                            "Не удалось получить информацию о путях из OpenAPI."
                        )
                else:
                    await callback.message.answer(
                        f"Ошибка при обращении к FastAPI: статус {response.status}"
                    )
        except Exception as e:
            await callback.message.answer(f"Произошла ошибка при обращении к FastAPI: {str(e)}")

dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
