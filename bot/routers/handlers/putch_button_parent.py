import os
import os.path
from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (KeyboardButton,
                           Message,
                           ReplyKeyboardMarkup)
from routers.crud import get_button_content, putch_button_parent
from routers.tree_commands import send_tree
from .base import (base_reply_markup,
                   cancel_and_return_to_admin_panel,
                   message_button_response,
                   validate_response)
from core.config import settings


API_URL = settings.api.base_url
# API_URL = os.getenv("API_URL")
router = Router()


class PutchButtonParent(StatesGroup):
    typing_button_id = State()
    typed_new_parent_id = State()
    submiting_update_parent = State()


@router.callback_query(F.data == "putch_button_parent")
async def handle_del_button(callback: types.CallbackQuery, state: FSMContext):
    await send_tree(callback.message)
    await callback.message.answer(
        text="Введите кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(PutchButtonParent.typing_button_id)


@router.message(PutchButtonParent.typing_button_id)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    response = await get_button_content(int(message.text))
    if not await validate_response(response, message, state):
        return
    await state.update_data(typed_button_id=message.text)
    await message.answer(
        text="Теперь введите айди новой кнопки-родителя:",
        reply_markup=base_reply_markup,
    )
    await state.set_state(PutchButtonParent.typed_new_parent_id)


@router.message(PutchButtonParent.typed_new_parent_id)
async def parent_id_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_new_parent_id=message.text)
    user_data = await state.get_data()
    new_reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 Обновить родительскую кнопку")]]
        + base_reply_markup.keyboard,
        resize_keyboard=True,
    )
    response = await get_button_content(user_data["typed_button_id"])
    if not await validate_response(response, message, state):
        return

    button = response.json()
    await message.answer(
        text=(
            f"Обновляю?\n"
            f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
            f"Айди новой кнопки-родителя:"
            f"<b>{user_data['typed_new_parent_id']}</b>\n"
        ),
        reply_markup=new_reply_markup,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(PutchButtonParent.submiting_update_parent)


@router.message(PutchButtonParent.submiting_update_parent)
async def button_submited(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    user_data = await state.get_data()
    button_id = user_data["typed_button_id"]
    new_parent_id = user_data["typed_new_parent_id"]

    response = await putch_button_parent(button_id, new_parent_id)
    if await message_button_response(response, message, state):
        await cancel_and_return_to_admin_panel(message, state)
