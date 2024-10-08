import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not API_TOKEN:
    raise ValueError("Не найден токен бота. Пожалуйста, добавьте TELEGRAM_BOT_TOKEN в .env файл.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


admin_start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поздороваться", callback_data="greet")],
        [InlineKeyboardButton(text="Сказать пока", callback_data="say_bye")],
        [
            InlineKeyboardButton(text="Перейти на сайт 1", url="https://example1.com"),
            InlineKeyboardButton(text="Перейти на сайт 2", url="https://example2.com")
        ],
        [InlineKeyboardButton(text="Показать уведомление", callback_data="show_alert")]
    ])


admin_start_keyboard_structure = {
    "admin_block_start_message": "Разделы админки:",
    "main_menu": {
        "buttons": [
            {"text": "Создать кнопку", "callback_data": "post_button"},
            {"text": "Получить контент кнопки", "callback_data": "get_button_content"},
            {"text": "Получить все дочерние кнопки", "callback_data": "get_button_subs"},
            {"text": "Изменить контент кнопки", "callback_data": "putch_button_content"},
            {"text": "Изменить родителя кнопки", "callback_data": "putch_button_head"},
            {"text": "Удалить кнопку", "callback_data": "delete_button"}
        ]
    }
}


def generate_main_menu(buttons_structure):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button['text'], callback_data=button['callback_data'])]
        for button in buttons_structure['main_menu']['buttons']
    ])
    return keyboard


@dp.message(Command(commands=['admin']))
async def show_base_admin_panel(message: types.Message):
    await message.answer(
        # "Привет! Нажми на кнопку для входа в админку.",
        admin_start_keyboard_structure['admin_block_start_message'],
        # reply_markup=admin_start_keyboard
        reply_markup=generate_main_menu(admin_start_keyboard_structure)
    )


@dp.message(Command(commands=['help']))
async def send_help_info(message: types.Message):
    await message.answer(
        "Привет! Тут все просто. Нажми /start и нажимай на кнопки."
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
