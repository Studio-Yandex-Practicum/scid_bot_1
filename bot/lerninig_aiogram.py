import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import F
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not API_TOKEN:
    raise ValueError("Не найден токен бота. Пожалуйста, добавьте TELEGRAM_BOT_TOKEN в .env файл.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def get_greeting_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поздороваться", callback_data="greet")],
        [InlineKeyboardButton(text="Сказать пока", callback_data="say_bye")]
    ])
    return keyboard


@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку, чтобы получить приветствие.",
        reply_markup=get_greeting_keyboard()
    )

@dp.callback_query(F.data == "greet")
async def handle_greet(callback: types.CallbackQuery):
    user_first_name = callback.from_user.first_name
    greeting_message = f"Привет, {user_first_name}!"
    await callback.message.answer(greeting_message)
    await callback.answer()


@dp.callback_query(F.data == "say_bye")
async def handle_say_bye(callback: types.CallbackQuery):
    user_first_name = callback.from_user.first_name
    greeting_message = f"Пока, {user_first_name}!"
    await callback.message.answer(greeting_message)
    await callback.answer()


@dp.message(Command(commands=['help']))
async def send_help_info(message: types.Message):
    await message.answer(
        "Привет! Тут все просто. Нажми /start и нажимай на кнопки."
    )


@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer(
        "Нажми /start или /help."
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
