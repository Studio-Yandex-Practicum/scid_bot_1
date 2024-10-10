import logging
import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message, ReplyKeyboardRemove



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


# пробую получить название кнопки

class CreateButton(StatesGroup):
    typing_button_name = State()
    typing_parent_id = State()


# base_reply_markup = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Назад", callback_data="back")],
#             [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
#         ])


base_reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад")],
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,  # Опционально: делает клавиатуру компактной
    # one_time_keyboard=True  # Опционально: убирает клавиатуру после нажатия
)


# @dp.callback_query(F.data == "post_button")
# async def handle_post_button(callback: types.CallbackQuery):
#     await callback.message.answer("Введите название новой кнопки")
#     await callback.answer()


@dp.callback_query(F.data == "post_button")
async def handle_post_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите название новой кнопки",
        reply_markup=base_reply_markup
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CreateButton.typing_button_name)


# @dp.message(Command("post_button"))
# async def cmd_food(message: Message, state: FSMContext):
#     await message.answer(
#         text="Введите название новой кнопки",
#         reply_markup=base_reply_markup
#     )
#     # Устанавливаем пользователю состояние "выбирает название"
#     await state.set_state(CreateButton.typing_button_name)


@dp.message(CreateButton.typing_button_name)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(typed_name=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите айди кнопки-родителя:",
        reply_markup=base_reply_markup
    )
    await state.set_state(CreateButton.typing_parent_id)


@dp.message(CreateButton.typing_parent_id)
async def parent_id_chosen(message: Message, state: FSMContext):
    # await state.update_data(typed_id=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=f"{message.text}{user_data['typed_name']}",
        # reply_markup=base_reply_markup
    )
    await state.set_state(CreateButton.typing_parent_id)


# проверка, что кнопка работает
@dp.callback_query(F.data == "get_button_content")
async def handle_get_button_content(callback: types.CallbackQuery):
    await callback.message.answer("ты нажал вторую кнопку")
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
