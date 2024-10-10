from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.common_keyboards import (fetch_buttons_from_api,
                                        fetch_buttons_from_api_TEST,
                                        generate_keyboard
                                        )

router = Router()


# Функция для добавления кнопки "Назад"
def add_back_button(keyboard: InlineKeyboardMarkup, previous_id: int):
    back_button = InlineKeyboardButton(
        text="Назад",
        callback_data=f"callback_back_{previous_id}"
    )
    keyboard.inline_keyboard.append([back_button])
    return keyboard


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
            keyboard = await generate_keyboard(buttons)
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
                buttons_data = await fetch_buttons_from_api_TEST(endpoint_id=1)
                keyboard = await generate_keyboard(buttons_data)
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
