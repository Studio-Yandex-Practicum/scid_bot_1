from datetime import datetime, timezone
from typing import Any, Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext

from api.api_managers import get_all_orders_for_manager
from utils.manager_state import ManagerState


async def remove_previous_message(
    bot: Bot,
    data: dict[str, Any],
    chat_id: int
):
    await bot.delete_message(
        message_id=data['prev_message_id'],
        chat_id=chat_id
    )


async def show_message(
    reply_keyboard: Optional[InlineKeyboardMarkup],
    state: FSMContext,
    new_state: Optional[ManagerState],
    message: Message,
    text: str,
    state_update_data: dict[str, Any] = {}
):
    if new_state:
        await state.set_state(new_state)
    await message.edit_text(
        text=text,
        reply_markup=reply_keyboard,
        parse_mode=ParseMode.HTML
    )
    await state.update_data(
        data=state_update_data,
    )


async def generate_order_text(
    order: dict[str, Any],
    preview: bool = True
) -> str:
    if order['contact_via_telegram']:
        contact_via = "-"
    if order['contact_via_phone']:
        contact_via = "телефон"
    if order['contact_via_email']:
        contact_via = "email"
    create_date = datetime.strptime(
        order['created_at'],'%Y-%m-%dT%H:%M:%S.%fZ'
    )
    create_date = create_date.replace(
        tzinfo=timezone.utc
    ).astimezone(tz=None)
    text = (
        f"Заявка: {datetime.strftime(create_date, '%d.%m.%Y %H:%M:%S')}\n\n"
        f"Связь через: {contact_via}\n\n"
        f"Вопрос: {order['text']}"
    )
    if not preview:
        text += "\n\n"
        text += (
            f"Телефон: {order['phone']}\n"
            f"email: {order['email']}\n"
        )
    return text