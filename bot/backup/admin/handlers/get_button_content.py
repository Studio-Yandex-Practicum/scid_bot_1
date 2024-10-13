from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from crud import get_button_content
from .base import cancel_and_return_to_admin_panel, base_reply_markup


router = Router()


class CreateButton(StatesGroup):
    typing_button_id = State()

@router.callback_query(F.data == "get_button_content")
async def handle_get_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите айди кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(CreateButton.typing_button_id)


@router.message(CreateButton.typing_button_id)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    # await state.update_data(typed_id=message.text)
    response = await get_button_content(message.text)
    button = response.json()
    print(button)
    if response.status_code == 200:
        await message.answer(
            text=(
                f"контент кнопки:\n"
                f"Текст на кнпоке: <b>{button['label']}</b>\n"
                f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
                f"Текст сообщения над кнопкой: <b>{button['content_text']}</b>\n"
                f"Линк кнопки: <b>{button['content_link']}</b>\n"
                # f"Изображение: <b>{button['content_image']}</b>"
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.answer(text=(button["detail"]))

    await cancel_and_return_to_admin_panel(message, state)
