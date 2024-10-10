import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram import Router
from magic_filter import F
import asyncio
import logging
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
# API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN2")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
user_data = {}


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None


# Нажатие на одну из кнопок: -2, -1, +1, +2
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callbacks_num_change_fab(
    callback: types.CallbackQuery, callback_data: NumbersCallbackFactory
):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text_fab(
        callback.message, user_value + callback_data.value
    )
    await callback.answer()


# Нажатие на кнопку "подтвердить"
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="-2",
        callback_data=NumbersCallbackFactory(action="change", value=-2),
    )
    builder.button(
        text="-1",
        callback_data=NumbersCallbackFactory(action="change", value=-1),
    )
    builder.button(
        text="+1",
        callback_data=NumbersCallbackFactory(action="change", value=1),
    )
    builder.button(
        text="+2",
        callback_data=NumbersCallbackFactory(action="change", value=2),
    )
    builder.button(
        text="Подтвердить",
        callback_data=NumbersCallbackFactory(action="finish"),
    )
    # Выравниваем кнопки по 4 в ряд, чтобы получилось 4 + 1
    builder.adjust(4)
    return builder.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}", reply_markup=get_keyboard_fab()
    )


@dp.message(Command("numbers_fab"))
async def cmd_numbers_fab(message: types.Message):
    # print(message)
    user_data[message.from_user.id] = 0
    # print(user_data)
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())


# @dp.callback_query(NumbersCallbackFactory.filter())
# async def callbacks_num_change_fab(
#         callback: types.CallbackQuery,
#         callback_data: NumbersCallbackFactory
# ):
#     user_value = user_data.get(callback.from_user.id, 0)
#     if callback_data.action == "change":
#         user_data[callback.from_user.id] = user_value + callback_data.value
#         await update_num_text_fab(callback.message, user_value + callback_data.value)
#     # Если число нужно зафиксировать
#     else:
#         await callback.message.edit_text(f"Итого: {user_value}")
#     await callback.answer()


@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer("Нажми /start или /help.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
