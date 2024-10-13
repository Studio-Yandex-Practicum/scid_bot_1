from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from crud import get_child_buttons
from .base import cancel_and_return_to_admin_panel, base_reply_markup


router = Router()


class CreateButton(StatesGroup):
    typing_button_idd = State()

@router.callback_query(F.data == "get_child_buttons")
async def handle_get_child_buttons(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите айди кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(CreateButton.typing_button_idd)


@router.message(CreateButton.typing_button_idd)
async def show_child_buttons(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    response = await get_child_buttons(message.text)
    buttons = response.json()
    if response.status_code == 200:
        buttons_text = ""
        for button in buttons:
            button_info = f"{button['label']} ({button['id']})"
            buttons_text += button_info + "\n"

        await message.answer(
            text=buttons_text,
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(text=(buttons["detail"]))

    await cancel_and_return_to_admin_panel(message, state)
