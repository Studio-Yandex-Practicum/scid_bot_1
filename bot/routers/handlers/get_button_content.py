from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from routers.crud import get_button_content
from routers.tree_commands import send_tree
from .base import (base_reply_markup,
                   cancel_and_return_to_admin_panel,
                   message_button_response)

router = Router()


class GetButtonContent(StatesGroup):
    typing_button_id = State()


@router.callback_query(F.data == "get_button_content")
async def handle_get_button(callback: types.CallbackQuery, state: FSMContext):
    await send_tree(callback.message)
    await callback.message.answer(
        text="Введите кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(GetButtonContent.typing_button_id)


@router.message(GetButtonContent.typing_button_id)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    response = await get_button_content(message.text)
    if await message_button_response(response, message, state):
        await cancel_and_return_to_admin_panel(message, state)
