from aiogram import types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.admin import generate_main_menu


async def show_base_admin_panel(message: types.Message):
    await message.answer(
        "Админ-панель SCID_BOT_1",
        reply_markup=await generate_main_menu(),
    )


async def cancel_and_return_to_admin_panel(
    message: Message, state: FSMContext
):
    await state.clear()
    await message.answer(
        "Возвращаюсь в основное меню", reply_markup=types.ReplyKeyboardRemove()
    )
    await show_base_admin_panel(message, state)
