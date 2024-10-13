from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для генерации клавиатуры - Меню из кнопок
async def inline_menu(buttons, columns=1, start_id=1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        button_id = button.get("id")
        parent_id = button.get("parent_id", start_id)
        label = button.get("label", "Без названия")
        keyboard.add(InlineKeyboardButton(
            text=label,
            callback_data=f"{button_id},{parent_id}"
        ))
    keyboard.adjust(columns)
    if buttons:
        parent_id = buttons[0].get('parent_id', start_id)
        if parent_id != start_id:
            keyboard.add(InlineKeyboardButton(
                text="Назад", callback_data=f"{parent_id},back"
            ))
    keyboard.add(InlineKeyboardButton(
        text="В начало", callback_data=f"{start_id},home"
    ))
    keyboard.adjust(1)
    return keyboard.as_markup()
