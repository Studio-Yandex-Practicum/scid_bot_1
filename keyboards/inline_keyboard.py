from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_menu(buttons, columns=2, start_id=1) -> InlineKeyboardMarkup:
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

    columns = Buttons in row

    callback_data = "button_id:int,parent_id:int"
    Examples:
        callback_data = "3,2"
        callback_data = "2" # Back
    """

    keyboard = InlineKeyboardBuilder()

    for button in buttons:
        keyboard.add(
            InlineKeyboardButton(
                text=button["label"],
                callback_data=(f"{button['id']}," f"{button['parent_id']}"),
            )
        )
    keyboard.adjust(columns)
    # Service keyboard ("Back" and "to start").
    # One Button at row
    parent_id = buttons[0].get("parent_id")
    service_keyboard = InlineKeyboardBuilder()
    service_keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data=(f"{parent_id}"))
    )
    service_keyboard.add(
        InlineKeyboardButton(text="В начало", callback_data=(f"{start_id}"))
    )
    service_keyboard.adjust(1)

    keyboard.attach(service_keyboard)
    return keyboard.as_markup()
