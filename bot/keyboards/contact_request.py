from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

class ContactViaType(str, Enum):
    tg = "телеграм"
    phone = "телефон"
    email = "e-mail"

    def __str__(self) -> str:
        return self.value


class ContactViaCallback(CallbackData, prefix="contact_via"):
    contact_type: ContactViaType


def generate_reply_keyboard_from_structure(
    resize_keyboard: bool = True,
    one_time_keyboard: bool = True,
    input_field_placeholder: str = "Воспользуйтесь меню:",
    structure: list[dict | KeyboardButton]  = []
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=button['text'],
                    request_contact=button['request_contact']
                ) if isinstance(button, dict) else button
            ] for button in structure
        ],
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder
    )

CANCEL_BUTTON = KeyboardButton(
    text="🔚 Отменить запрос на обратную связь"
)

CONTACT_REQUEST_START_BUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❓ Задать вопрос менеджеру",
                callback_data="start_contact_request"
            )
        ]
    ]
)

CONTACT_REQUEST_CONTACT_VIA_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⭐ Телеграм (должен быть указан @Имя_пользователя)",
                callback_data=ContactViaCallback(
                    contact_type=ContactViaType.tg
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="☎️ Телефон",
                callback_data=ContactViaCallback(
                    contact_type=ContactViaType.phone
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="📧 E-mail",
                callback_data=ContactViaCallback(
                    contact_type=ContactViaType.email
                ).pack()
            )
        ]
    ]
)

CONTACT_REQUEST_GET_PHONE_BUTTON_STRUCTURE = [
    {
        "text":"☎️ Отправить номер телефона",
        "request_contact":True
    },
    {
        "text":"📵 Не отправлять номер телефона",
        "request_contact":False
    },
    CANCEL_BUTTON
]

CONTACT_REQUEST_GET_EMAIL_BUTTON_STRUCTURE = [
    {
        "text":"🚫 Не отправлять e-mail",
        "request_contact":False
    },
    CANCEL_BUTTON
]

CONTACT_REQUEST_SEND_REQUEST_STRUCTURE = [
    {
        "text":"📫 Отправить заявку",
        "request_contact":False
    },
    CANCEL_BUTTON
]

CONTACT_REQUEST_CANCEL_MENU = generate_reply_keyboard_from_structure(
    structure=[CANCEL_BUTTON]
)

CONTACT_REQUEST_GET_PHONE_BUTTON = generate_reply_keyboard_from_structure(
    structure=CONTACT_REQUEST_GET_PHONE_BUTTON_STRUCTURE
)

CONTACT_REQUEST_GET_EMAIL_BUTTON = generate_reply_keyboard_from_structure(
    structure=CONTACT_REQUEST_GET_EMAIL_BUTTON_STRUCTURE
)

CONTACT_REQUEST_SEND_REQUEST_MENU = generate_reply_keyboard_from_structure(
    structure=CONTACT_REQUEST_SEND_REQUEST_STRUCTURE
)