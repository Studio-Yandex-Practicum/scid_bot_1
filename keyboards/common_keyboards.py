# Обычные клавиатуры
import aiohttp

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.filters.callback_data import CallbackData

API_URL = 'https://your-api-endpoint.com'

# Используем вспомогательный класс CallbackData
# action - какое будет выполняться действие
# value - что связано с действием
# extra - доп инфа
class ButtonCallback(CallbackData, prefix="action"):
    value: str
    extra_info: str


def get_start_keyboard():
    button1 = InlineKeyboardButton(
        text="🔥 Яндекс",
        callback_data=ButtonCallback(value="btn1",
                                     extra_info="info1").pack()
    )
    button2 = InlineKeyboardButton(
        text="🔥 Google",
        url="https://google.com/",
    )
    # Кнопки в ряд
    row = [button1, button2]
    # Ряд кнопок
    rows = [row]
    # Инциализируем клавиатуру
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


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