from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_menu(button: dict, start_id: int) -> InlineKeyboardMarkup:
    """
    button example:
    button =
        {
            "id": 3,
            "label": "test_1",
            "parent_id": 2
        }
    callback_data examples:

    callback_data = "button_id:int,parent_id:int"
        for normal button
        callback_data = "3,2"

        for "Back" button
        callback_data = "2"
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=button["label"],
                                      callback_data=(
                                          f"{button['id']},"
                                          f"{button['parent_id']}")))
   # Service keyboard ("Back" and "to start").
    # One Button at row

    service_keyboard = InlineKeyboardBuilder()
    service_keyboard.add(InlineKeyboardButton(text="Назад",
                                              callback_data=(
                                                  f"{button['parent_id']}")))
    service_keyboard.add(InlineKeyboardButton(text="В начало",
                                              callback_data=(
                                                  f"{start_id}")))
    service_keyboard.adjust(1)

    keyboard.attach(service_keyboard)
    return keyboard.as_markup()
