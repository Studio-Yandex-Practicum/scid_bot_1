from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from api.api_main_button import get_api_data
from keyboards.board_main_button import make_main_button_keyboard

router = Router() # создаем роутер для обработки команд

comm = ["Получить данные кнопки", "Проверить работу API"]

@router.message(Command(commands=["main_button"]))
async def cmd_main_button(message: Message):
    await message.answer(
        text="Выберите команду:",
        reply_markup=make_main_button_keyboard(comm)
    )


@router.message(F.text.in_(comm))
async def handle_command(message: Message):
    data = await get_api_data()
    if not data:
        await message.answer("Не удалось получить данные от API.")
        return

    if message.text == "Получить данные кнопки":
        label = data.get("label")
        button_id = data.get("id")
        text_message = (
            f"<b>Кнопка: {label}</b>\n\n"
            f"ID: {button_id}\n\n"
        )
        await message.answer(text_message, parse_mode="HTML")
    elif message.text == "Проверить работу API":
        await message.answer("Данные получены!")
