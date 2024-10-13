from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from api.api_main_button import get_api_data
from api.api_points import handle_menu_get_main_menu_button
from keyboards.common_keyboards import inline_menu

# создаем роутер для обработки команд
router = Router()

comm = ["Получить данные кнопки", "Проверить работу API"]

# Хендлер для команды /main_button
@router.message(Command(commands=["main_button"]))
async def cmd_main_button(message: Message):
    # Получаем основное меню через API
    main_menu = await handle_menu_get_main_menu_button()

    if not main_menu or not isinstance(main_menu, list):
        await message.answer("Не удалось получить данные от API.")
        return

    # Создаем динамическую клавиатуру из полученных данных
    keyboard = await inline_menu(main_menu, start_id=1)

    # Отправляем сообщение с клавиатурой
    await message.answer(
        text="Выберите команду:",
        reply_markup=keyboard
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
