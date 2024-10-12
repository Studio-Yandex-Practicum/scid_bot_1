# Обычные клавиатуры
import aiohttp

from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from bot.keyboards.common_keyboards import (
    inline_menu,
    add_back_button,
    fetch_buttons_from_api
)

API_URL = 'https://your-api-endpoint.com'

# Используем вспомогательный класс CallbackData
# action - какое будет выполняться действие
# value - что связано с действием
# extra - доп инфа
class ButtonCallback(CallbackData, prefix="action"):
    value: str
    extra_info: str

# Хендлер для обработки нажатий на кнопки
@router.callback_query(lambda c: c.data.startswith('callback_'))
async def callback_handler(callback_query: types.CallbackQuery):
    data_parts = callback_query.data.split('_')
    action = data_parts[1]

    # Обработка кнопки "Назад"
    if action == "back":
        previous_id = int(data_parts[2])

        # Возвращаемся к предыдущему меню
        if previous_id == 0:
            # Если previous_id == 0, то это главное меню
            buttons = [
                {"id": 1, "name": "Получить информацию о компании", "url": None},
                {"id": 2, "name": "Узнать о продуктах и услугах", "url": None},
                {"id": 3, "name": "Получить техническую поддержку", "url": None},
                {"id": 4, "name": "Посмотреть портфолио", "url": None},
                {"id": 5, "name": "Связаться с менеджером", "url": None},
            ]
            keyboard = await inline_menu(buttons)
            await callback_query.message.edit_text(
                "Здравствуйте! Я ваш виртуальный помощник. Как я могу помочь вам сегодня?",
                reply_markup=keyboard
            )
        else:
            # Можно добавить логику для возврата в другие подменю, если необходимо
            await callback_query.message.edit_text(
                f"Возврат в меню с ID {previous_id}.",
                reply_markup=types.InlineKeyboardMarkup()  # Замените на нужную клавиатуру для этого ID
            )
    else:
        try:
            # Преобразуем button_id в число
            button_id = int(data_parts[-1])

            # Обработка конкретных кнопок меню
            if button_id == 1:
                # Используем тестовую функцию для загрузки кнопок для информации о компании
                buttons = await fetch_buttons_from_api(endpoint_id=1)
                keyboard = await inline_menu(buttons)
                # Добавляем кнопку "Назад" с ID главного меню (0)
                keyboard = add_back_button(keyboard, previous_id=0)
                await callback_query.message.edit_text(
                    "Информация о компании:",
                    reply_markup=keyboard
                )
            # Можно добавить другие условия для обработки button_id

        except ValueError:
            print("Неверный формат callback_data")

    # Закрываем уведомление о нажатии кнопки
    await callback_query.answer()
