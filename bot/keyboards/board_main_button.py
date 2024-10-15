from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def make_main_button_keyboard(items: list[str]) -> ReplyKeyboardMarkup:

    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
