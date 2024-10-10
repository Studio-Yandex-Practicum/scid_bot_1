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
async def show_base_admin_panel(message: types.Message):
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


class Button(StatesGroup):
    name = State()
    parent = State()

# создать кнопку
# @dp.callback_query(F.data == "post_button")
# async def handle_post_button(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.answer("Йоу менчик, ща создам кнопку!")
#     await callback.message.answer("Введите имя кнопки:")
#     await state.set_state(Button.name)
#     # await Button.name.set()
#     await callback.answer()


# @dp.message(F.text, state=Button.name)
# async def process_button_name(message: types.Message, state: FSMContext):
#     button_name = message.text
#     await state.update_data(name=button_name)

#     await message.answer("Введите айди кнопки-родителя:")
#     # await Button.parent.set()
#     await state.set_state(Button.parent) 
#     # await state.update_data(content_text='string') #


# @dp.message(F.text, state=Button.parent)
# async def process_button_content(message: types.Message, state: FSMContext):
#     # content_text = message.text  #
#     parent = message.text
#     user_data = await state.get_data()
#     button_name = user_data['name']
#     print("ааааааааааааааааа")
#     print(button_name)
#     print(parent)
#     url = f'http://127.0.0.1/bot_menu/2/add-child-button'
#     headers = {
#         'accept': 'application/json',
#         'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3MjkxMjM4OTl9.llAqWSztLSDr7q33YcKzHpgXxb4sNAiX43zIyPuKvIw'
#         }
#     data = {
#         'label': button_name,
#         'content_text': 'string',
#         'content_link': 'string'
#         }
#     # files = {'content_image': open('/path/to/your/image.png', 'rb')}
#     response = requests.post(url, headers=headers, data=data)
#     # response = requests.post(url, headers=headers, data=data, files=files)
#     print(response.status_code)
#     print(response.json())
#     await message.answer("Кнопка успешно создана!")
#     await message.answer(response.json())
#     await state.finish()


# @dp.message(Command(commands=['get_button_content']))
# async def handle_get_button_content(message: types.Message):
#     await message.answer("get_button_content.")


@dp.callback_query(F.data == "get_button_content")
async def handle_get_button_content(callback: types.CallbackQuery):
    await callback.message.answer("get_button_content")
    # await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)
