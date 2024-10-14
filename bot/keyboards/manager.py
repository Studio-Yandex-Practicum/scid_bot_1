from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class OrderCallback(CallbackData, prefix="order"):
    to_work: bool
    current_order: int


MANAGER_MAIN_MENU_STRUCTURE = [
    {
        "text": "🗒️ Новые заявки",
        "callback_data": "new_order"
    },
    {
        "text": "📓 Заявки в работе",
        "callback_data": "managers_order",
    },
        {
        "text": "🔻 ЗАВЕРШИТЬ РАБОТУ",
        "callback_data": "managers_end_work",
    }
]


START_MANAGER_WORK = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔹 Начать работу 🔹",
                callback_data="manager_start_work"
            )
        ]
    ]
)


MANAGER_MAIN_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=button["text"], callback_data=button["callback_data"]
            )
        ]
        for button in MANAGER_MAIN_MENU_STRUCTURE
    ]
)


async def generate_order_keyboard(
    page: int = 0,
    orders_len: int = 0
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    has_next_page = orders_len >= page + 1
    navigate_buttons = [
        InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=OrderCallback(
                to_work=False,
                current_order=(page - 1) if page >= 1 else page
            ).pack()
        ),
        InlineKeyboardButton(
            text=f"• {page + 1}/{orders_len} •",
            callback_data=OrderCallback(
                to_work=False,
                current_order = page
            ).pack()
        ),
        InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=OrderCallback(
                to_work=False,
                current_order=(page + 1) if has_next_page else page
            ).pack()
        )
    ]
    keyboard.row(*navigate_buttons, width=3)
    keyboard.row(
        InlineKeyboardButton(
            text="📑 Взять в работу",
            callback_data=OrderCallback(
                to_work=True,
                current_order=page
            ).pack()
        ),
        width=1
    )
    keyboard.row(
        InlineKeyboardButton(
            text="⬆️ В главное меню",
            callback_data="go_to_start"
        ),
        width=1
    )
    return keyboard.as_markup()