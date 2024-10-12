# Обычные клавиатуры
import aiohttp

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_URL = ''


# Функция для добавления кнопки "Назад"
def add_back_button(keyboard: InlineKeyboardMarkup, previous_id: int):
    back_button = InlineKeyboardButton(
        text="Назад",
        callback_data=f"callback_back_{previous_id}"
    )
    keyboard.inline_keyboard.append([back_button])
    return keyboard


# Функция для генерации клавиатуры - Кнопки
async def fetch_buttons_from_api(endpoint_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/buttons/{endpoint_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('buttons', [])
                else:
                    return []
        except Exception as e:
            print(f"Error fetching buttons: {str(e)}")
            return []


# Функция для генерации клавиатуры - Меню из кнопок
async def inline_menu(buttons, columns=2, start_id=1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for button in buttons:
        keyboard.add(InlineKeyboardButton(
            text=button["label"],
            callback_data=f"{button['id']},{button['parent_id']}"
        ))
    keyboard.adjust(columns)

    # Добавляем служебные кнопки "Назад" и "В начало"
    parent_id = buttons[0].get('parent_id', start_id)
    keyboard.add(InlineKeyboardButton(
        text="Назад", callback_data=f"{parent_id}"
    ))
    keyboard.add(InlineKeyboardButton(
        text="В начало", callback_data=f"{start_id}"
    ))
    keyboard.adjust(1)

    return keyboard.as_markup()
