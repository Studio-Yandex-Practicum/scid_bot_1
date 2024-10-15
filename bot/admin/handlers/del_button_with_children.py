from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup)
from crud import (del_button_with_children, get_button_content,
                  get_child_buttons)

from .base import base_reply_markup, cancel_and_return_to_admin_panel

router = Router()


class DelButton(StatesGroup):
    typing_button_id = State()
    confirming_del = State()


@router.callback_query(F.data == "del_button_with_children")
async def handle_del_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите айди кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(DelButton.typing_button_id)


@router.message(DelButton.typing_button_id)
async def ask_for_confirmation(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_id=message.text)
    user_data = await state.get_data()
    response = await get_child_buttons(user_data["typed_id"])
    buttons = response.json()
    if response.status_code == 200:  # убрать
        buttons_text = ""
        for button in buttons:
            button_info = f"{button['label']} ({button['id']})"
            buttons_text += button_info + "\n"
        if buttons_text == "":
            buttons_text = "Нет дочерних кнопок"
    confirmation_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да")]] + base_reply_markup.keyboard,
        resize_keyboard=True,
    )
    await message.answer(
        text=(
            f"Вы уверены, что хотите удалить кнопку и все дочерние?\n"
            f"Дочерние кнопки:\n"
            f"{buttons_text}"
        ),
        reply_markup=confirmation_markup,
    )
    await state.set_state(DelButton.confirming_del)


@router.message(DelButton.confirming_del)
async def confirm_del_button(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    user_data = await state.get_data()
    await del_button_with_children(
        user_data["typed_id"]
    )
    await message.answer(text="Кнопка и все дочерние удалены")
    response = await get_button_content(user_data["typed_id"])
    await message.answer(text=f"{response.json()}")
    await cancel_and_return_to_admin_panel(message, state)
