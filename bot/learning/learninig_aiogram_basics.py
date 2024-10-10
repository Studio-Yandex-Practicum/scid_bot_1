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

# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN2")
if not API_TOKEN:
    raise ValueError(
        "Не найден токен бота. Пожалуйста, добавьте TELEGRAM_BOT_TOKEN в .env файл."
    )

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)


class Form(StatesGroup):
    name = State()
    age = State()


@dp.message(Command(commands=["fill"]))
async def cmd_fill(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    age = message.text

    if not age.isdigit():
        await message.answer(
            "Возраст должен быть числом. Пожалуйста, введите ваш возраст:"
        )
        return

    await message.answer(f"Приятно познакомиться, {name}! Вам {age} лет.")
    await state.clear()


def get_greeting_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Поздороваться", callback_data="greet"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Сказать пока", callback_data="say_bye"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Перейти на сайт 1", url="https://example1.com"
                ),
                InlineKeyboardButton(
                    text="Перейти на сайт 2", url="https://example2.com"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Показать уведомление", callback_data="show_alert"
                )
            ],
        ]
    )
    return keyboard


@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку, чтобы получить приветствие.",
        reply_markup=get_greeting_keyboard(),
    )


@dp.callback_query(F.data == "show_alert")
async def handle_show_alert(callback: types.CallbackQuery):
    await callback.answer("Это всплывающее уведомление!", show_alert=True)


@dp.callback_query(F.data == "greet")
async def handle_greet(callback: types.CallbackQuery):
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name or ""
    if user_last_name:
        greeting_message = f"Привет, {user_first_name} {user_last_name}!"
    else:
        greeting_message = f"Привет, {user_first_name}!"
    await callback.message.answer(greeting_message)
    await callback.answer()


@dp.callback_query(F.data == "say_bye")
async def handle_say_bye(callback: types.CallbackQuery):
    user_first_name = callback.from_user.first_name
    greeting_message = f"Пока, {user_first_name}!"
    await callback.message.answer(greeting_message)
    await callback.answer()


@dp.message(Command(commands=["help"]))
async def send_help_info(message: types.Message):
    await message.answer(
        "Привет! Тут все просто. Нажми /start и нажимай на кнопки."
    )


@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer("Нажми /start или /help.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
