from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class OrderCallback(CallbackData, prefix="order"):
    to_work: bool
    done: bool
    current_order: int
    order_id: int
    in_progress: bool


def generate_keyboard_from_structure(
    structure: list[dict]
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button["text"], callback_data=button["callback_data"]
                )
            ]
            for button in structure
        ]
    )


MAIN_MENU_BASE_TEXT = (
    "<b>Что Вы хотите увидеть?</b>\n\n"
    "<b>Новые заявки</b> - заявки, которые еще не приняты в работу\n"
    "<b>Заявки в работе</b> - заявки, которые Вы взяли в работу"
)


MAIN_MENU_BUTTON = InlineKeyboardButton(
    text="⬆️ В главное меню",
    callback_data="go_to_start"
)


MANAGER_MAIN_MENU_STRUCTURE = [
    {
        "text": "🗒️ Новые заявки",
        "callback_data": "new_order"
    },
    {
        "text": "📓 Заявки в работе",
        "callback_data": "in_process_orders",
    },
        {
        "text": "🔻 ЗАВЕРШИТЬ РАБОТУ",
        "callback_data": "managers_end_work",
    }
]


START_MANAGER_WORK_STRUCTURE = [
    {
        "text": "🔹 Начать работу 🔹",
        "callback_data": "manager_start_work"
    },
]


START_MANAGER_WORK = generate_keyboard_from_structure(
    START_MANAGER_WORK_STRUCTURE
)
MANAGER_MAIN_MENU = generate_keyboard_from_structure(
    MANAGER_MAIN_MENU_STRUCTURE
)


async def generate_order_work_keyboard(
    order_id: int
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="✅ Заявка выполнена",
            callback_data=OrderCallback(
                to_work=False,
                done=True,
                current_order=-999,
                order_id=order_id,
                in_progress=False
            ).pack()
        )
    )
    keyboard.row(MAIN_MENU_BUTTON)

    return keyboard.as_markup()


async def generate_order_keyboard(
    page: int = 0,
    orders_len: int = 0,
    in_progress: bool = False
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    has_next_page = orders_len >= page + 1
    navigate_buttons = [
        InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=OrderCallback(
                to_work=False,
                done=False,
                current_order=(page - 1) if page >= 1 else page,
                order_id=-1,
                in_progress=in_progress
            ).pack()
        ),
        InlineKeyboardButton(
            text=f"• {page + 1}/{orders_len} •",
            callback_data=OrderCallback(
                to_work=False,
                done=False,
                current_order = page,
                order_id=-1,
                in_progress=in_progress
            ).pack()
        ),
        InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=OrderCallback(
                to_work=False,
                done=False,
                current_order=(page + 1) if has_next_page else page,
                order_id=-1,
                in_progress=in_progress
            ).pack()
        )
    ]
    keyboard.row(*navigate_buttons, width=3)
    keyboard.row(
        InlineKeyboardButton(
            text="📑 Подробнее" if in_progress else "📑 Взять в работу",
            callback_data=OrderCallback(
                to_work=True,
                current_order=page,
                done=False,
                order_id=-1,
                in_progress=in_progress
            ).pack()
        ),
        width=1
    )
    keyboard.row(
        MAIN_MENU_BUTTON,
        width=1
    )
    return keyboard.as_markup()