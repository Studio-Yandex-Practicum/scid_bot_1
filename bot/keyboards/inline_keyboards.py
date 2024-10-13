from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_menu_keyboard(buttons, back_button=False, columns=1):
    """Создаёт клавиатуру на основе переданных кнопок."""
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.add(
            InlineKeyboardButton(
                text=button['label'],
                callback_data=str(button['id'])
            )
        )
    if back_button:
        keyboard.add(
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back")
        )
    keyboard.add(
        InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="main_menu"
        )
    )
    keyboard.adjust(columns)
    markup = keyboard.as_markup()
    return markup
