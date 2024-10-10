import logging
import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


load_dotenv()

# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN2')
if not API_TOKEN:
    raise ValueError("Не найден токен бота. Пожалуйста, добавьте TELEGRAM_BOT_TOKEN в .env файл.")

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

# меню с кнопками
admin_start_keyboard_structure = {
    "admin_block_start_message": "Разделы админки:",
    "main_menu": {
        "buttons": [
            {"text": "Создать кнопку", "callback_data": "post_button"},
            {"text": "Получить контент кнопки", "callback_data": "get_button_content"},
            {"text": "Получить все дочерние кнопки", "callback_data": "get_button_subs"},
            {"text": "Изменить контент кнопки", "callback_data": "putch_button_content"},
            {"text": "Изменить родителя кнопки", "callback_data": "putch_button_parent"},
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
        admin_start_keyboard_structure['admin_block_start_message'],
        reply_markup=generate_main_menu(admin_start_keyboard_structure)
    )


@dp.message(Command(commands=['start']))
async def show_start_panel(message: types.Message):
    await message.answer(
        admin_start_keyboard_structure['admin_block_start_message'],
        reply_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Поздороваться", callback_data="greet")],
            [InlineKeyboardButton(text="Поиск", switch_inline_query="начни искать")],
            [InlineKeyboardButton(text="Поиск в этом чате", switch_inline_query_current_chat="найди здесь")],
            [
                InlineKeyboardButton(text="Перейти на сайт 1", url="https://example1.com"),
                InlineKeyboardButton(text="Перейти на сайт 2", url="https://example2.com")
            ],
            [InlineKeyboardButton(text="Показать уведомление", callback_data="show_alert")]
        ])
    )


# проверка, что кнопки работают
@dp.callback_query(F.data == "get_button_content")
async def handle_get_button_content(callback: types.CallbackQuery):
    await callback.message.answer("ты нажал вторую кнопку")
    await callback.answer()


available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)
