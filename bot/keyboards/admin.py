from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

ADMIN_START_KEYBOARD_STRUCTURE = [
    {"text": "Создать кнопку", "callback_data": "post_button"},
    {
        "text": "Получить контент кнопки",
        "callback_data": "get_button_content",
    },
    {
        "text": "Получить все дочерние кнопки",
        "callback_data": "get_button_subs",
    },
    {
        "text": "Изменить контент кнопки",
        "callback_data": "putch_button_content",
    },
    {
        "text": "Изменить родителя кнопки",
        "callback_data": "putch_button_parent",
    },
    {"text": "Удалить кнопку", "callback_data": "delete_button"},
]

BASE_REPLY_MARKUP = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True
)

NOT_REQUIRED_REPLY_MARKUP = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]]
    + BASE_REPLY_MARKUP.keyboard,
    resize_keyboard=True,
)


async def add_create_button_to_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Создать кнопку")]]
        + BASE_REPLY_MARKUP.keyboard,
        resize_keyboard=True,
    )


async def generate_main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button["text"], callback_data=button["callback_data"]
                )
            ]
            for button in ADMIN_START_KEYBOARD_STRUCTURE
        ]
    )
    return keyboard