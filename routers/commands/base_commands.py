from aiogram import Router, types
from aiogram.filters import Command
from keyboards.common_keyboards import generate_keyboard


router = Router()

# Хендлер для команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    buttons = [
        {"id": 1, "name": "Получить информацию о компании", "url": None},
        {"id": 2, "name": "Узнать о продуктах и услугах", "url": None},
        {"id": 3, "name": "Получить техническую поддержку", "url": None},
        {"id": 4, "name": "Посмотреть портфолио", "url": None},
        {"id": 5, "name": "Связаться с менеджером", "url": None},
    ]
    keyboard = await generate_keyboard(buttons)
    await message.answer(
        "Здравствуйте! Я ваш виртуальный помощник. Как я могу помочь вам сегодня?",
        reply_markup=keyboard,
    )
