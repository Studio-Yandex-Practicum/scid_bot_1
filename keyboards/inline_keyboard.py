from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



async def inline_menu(buttons: list[dict[str, int, str]]) -> InlineKeyboardMarkup:
    """
    buttons = [
    {
        "id": 3,
        "label": "test_1",
        "parent_id": 2
    },
    {
        "id": 4,
        "label": "test 2",
        "parent_id": 2
    }
    ]
    """


    keyboard = InlineKeyboardBuilder()

    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button["label"],
                                          callback_data=f""
                                                        f"{button['id'], button['parent_id']}"))
    keyboard.adjust(2)

    service_keyboard = InlineKeyboardBuilder()
    service_keyboard.add(InlineKeyboardButton(text="Назад",
                                           callback_data='2'))
    service_keyboard.add(InlineKeyboardButton(text="В начало",
                                           callback_data="1"))
    service_keyboard.adjust(1)

    keyboard.attach(service_keyboard)
    return keyboard.as_markup()
