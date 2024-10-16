from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup)
from routers.crud import (del_button_with_sub, get_child_buttons)
from routers.tree_commands import send_tree
from .base import (base_reply_markup,
                   cancel_and_return_to_admin_panel,
                   validate_response)

router = Router()


class DelButton(StatesGroup):
    typing_button_id = State()
    confirming_del = State()


@router.callback_query(F.data == "del_button_with_sub")
async def handle_del_button(callback: types.CallbackQuery, state: FSMContext):
    await send_tree(callback.message)
    await callback.message.answer(
        text="Введите кнопки", reply_markup=base_reply_markup
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
    if not await validate_response(response, message, state):
        return

    buttons = response.json()
    buttons_text = ("\n".join(
        f"{button['label']} ({button['id']})" for button in buttons)
        or "Нет дочерних кнопок")
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
    response = await del_button_with_sub(user_data["typed_id"])
    if response.status_code == 200:
        await message.answer(text="Кнопка и все дочерние удалены")
    else:
        try:
            detail = response.json().get("detail", "Неизвестная ошибка")
            await message.answer(text=detail)
        except (KeyError, ValueError):
            await message.answer("Ошибка. Не удалось получить ответ с сервера.")
        except Exception:
            await message.answer("Ошибка. Эту кнопку удалить не удалось.")
            print()
    await cancel_and_return_to_admin_panel(message, state)
