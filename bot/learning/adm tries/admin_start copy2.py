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

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not API_TOKEN:
    raise ValueError("Не найден токен бота. Пожалуйста, добавьте TELEGRAM_BOT_TOKEN в .env файл.")

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)


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


class Button(StatesGroup):
    name = State()
    parent = State()


@dp.callback_query(F.data == "post_button")
async def handle_say_bye(callback: types.CallbackQuery):
    await callback.message.answer("Йоу менчик, ща создам кнопку!")
    await callback.message.answer("Введи текст, который будет на кнопке")
    await state.set_state(Form.name)
    await state.update_data(name=message.text)
    await callback.message.answer("Введи айди родителя кнопки")
    await state.set_state(Form.parent)
    await state.update_data(parent=message.text)
    name = user_data.get('name')
    parent = user_data.get('parent')
    url = f'http://127.0.0.1/bot_menu/{parent}/add-child-button'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3MjkxMjM4OTl9.llAqWSztLSDr7q33YcKzHpgXxb4sNAiX43zIyPuKvIw'
        }
    data = {
        'label': name,
        'content_text': 'string',
        'content_link': 'string'
        }
    # files = {'content_image': open('/path/to/your/image.png', 'rb')}
    response = requests.post(url, headers=headers, data=data)
    # response = requests.post(url, headers=headers, data=data, files=files)
    print(response.status_code)
    print(response.json())
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
