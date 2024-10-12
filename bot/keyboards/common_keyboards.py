from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для генерации клавиатуры - Меню из кнопок
async def inline_menu(buttons, columns=2, start_id=1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    # Добавляем кнопки на основе данных из API
    for button in buttons:
        button_id = button.get("id")
        parent_id = button.get("parent_id", start_id)
        label = button.get("label", "Без названия")

        # Формируем кнопку с передачей ID и родительского ID через callback_data
        keyboard.add(InlineKeyboardButton(
            text=label,
            callback_data=f"{button_id},{parent_id}"
        ))

    # Настраиваем количество колонок
    keyboard.adjust(columns)

    # Добавляем служебные кнопки "Назад" и "В начало"
    if buttons:
        parent_id = buttons[0].get('parent_id', start_id)

        # Кнопка "Назад" появляется только если мы не находимся в корневом меню
        if parent_id != start_id:
            keyboard.add(InlineKeyboardButton(
                text="Назад", callback_data=f"{parent_id},back"
            ))

    # Кнопка "В начало"
    keyboard.add(InlineKeyboardButton(
        text="В начало", callback_data=f"{start_id},home"
    ))

    # Настраиваем клавиатуру для служебных кнопок
    keyboard.adjust(1)

    return keyboard.as_markup()
