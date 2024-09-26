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
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Загружаем токен и URL FastAPI из переменных окружения
TOKEN = os.getenv('TOKEN')  # Токен вашего Telegram-бота
API_URL = os.getenv('API_URL')  # URL FastAPI

if not TOKEN or not API_URL:
    raise ValueError("Переменные окружения TOKEN или API_URL не установлены!")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём объект Router для обработки команд
router = Router()

# Команда /start для приветствия и отображения кнопки


@router.message(Command("start"))
async def send_welcome(message: Message):
    # Создаем кнопку для вызова команды API
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Получить данные API", callback_data="call_api")]
        ]
    )

    await message.answer("Да работаю я, успокойся уже!", reply_markup=keyboard)

# Обработчик для нажатия кнопки с callback data "call_api"


@router.callback_query(lambda c: c.data == 'call_api')
async def call_api_callback(callback: CallbackQuery):
    await callback.message.answer("Обращаюсь к FastAPI...")

    # Выполняем запрос к FastAPI
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/api") as response:
                if response.status == 200:
                    data = await response.json()  # Парсим JSON-ответ
                    # Отправляем результат пользователю
                    await callback.message.answer(f"Ответ от FastAPI: {data}")
                else:
                    await callback.message.answer(
                        "Ошибка при обращении к FastAPI:"
                        f" статус {response.status}"
                    )
        except Exception as e:
            await callback.message.answer(
                f"Произошла ошибка при обращении к FastAPI: {str(e)}"
            )

# Регистрируем роутер в диспетчере
dp.include_router(router)

# Основная функция для запуска бота


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
