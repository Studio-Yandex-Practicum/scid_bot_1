import os
import os.path  # убрать протестить

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from crud import putch_button_content

from .base import (cancel_and_return_to_admin_panel,
                   base_reply_markup,
                   not_required_reply_markup,
                   handle_photo_upload,
                   message_button_response)


API_URL = os.getenv("API_URL")

router = Router()


class PutchButtonContent(StatesGroup):
    typing_button_id = State()
    typing_button_name = State()
    typing_parent_id = State()
    typing_content_text = State()
    typing_content_link = State()
    adding_content_image = State()
    submiting_update_button_content = State()


@router.callback_query(F.data == "putch_button_content")
async def handle_del_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите айди кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(PutchButtonContent.typing_button_id)


@router.message(PutchButtonContent.typing_button_id)
async def save_button_id(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_button_id=message.text)
    await message.answer(
        text="Введите название кнопки (можно пропустить)",
        reply_markup=not_required_reply_markup,
    )
    await state.set_state(PutchButtonContent.typing_button_name)


@router.message(PutchButtonContent.typing_button_name)
async def save_button_name(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        await state.update_data(typed_name=message.html_text)
    await message.answer(
        text="Теперь введите текст сообщения над кнопкой (можно пропустить):",
        reply_markup=not_required_reply_markup,
    )
    await state.set_state(PutchButtonContent.typing_content_text)


@router.message(PutchButtonContent.typing_content_text)
async def save_button_text(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        await state.update_data(typed_content_text=message.html_text)
    await message.answer(
        text="Теперь отправьте линк кнопки (можно пропустить):",  # где будет этот линк?
        reply_markup=not_required_reply_markup,
    )
    await state.set_state(PutchButtonContent.typing_content_link)


@router.message(PutchButtonContent.typing_content_link)
async def save_button_link(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        await state.update_data(typed_content_link=message.text)
    plus_del_reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Убрать изображение")]]
        + not_required_reply_markup.keyboard,
        resize_keyboard=True,
    )
    await message.answer(
        text="Теперь отправьте изображение, "
        "которое будет над кнопкой (можно пропустить):",
        reply_markup=plus_del_reply_markup,
    )
    await state.set_state(PutchButtonContent.adding_content_image)


@router.message(PutchButtonContent.adding_content_image)
async def save_button_image(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Убрать изображение":
        await state.update_data(remove_content_image="true")
    if message.text != "Пропустить":
        photo_id = await handle_photo_upload(message, state)

    user_data = await state.get_data()
    new_reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 Обновить кнопку")]]
        + base_reply_markup.keyboard,
        resize_keyboard=True,
    )

    await message.answer(
        text=(
            f"Все готово, осталось подтвердить:\n"
            f"Текст на кнопке: <b>{user_data['typed_name']}</b>\n"
            f"Текст сообщения над кнопкой:\n"
            f"{user_data.get('typed_content_text', '')}\n"
            f"Линк кнопки: <b>{user_data.get('typed_content_link', '')}</b>\n"
            f"Изображение:"
        ),
        reply_markup=new_reply_markup,
        parse_mode=ParseMode.HTML,
    )
    if "sent_content_image" in user_data:
        await message.answer_photo(photo=photo_id)

    await state.set_state(PutchButtonContent.submiting_update_button_content)


@router.message(PutchButtonContent.submiting_update_button_content)
async def button_submited(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return

    user_data = await state.get_data()

    button_id = user_data["typed_button_id"]
    data = {
        "label": user_data.get("typed_name", ""),
        "content_text": user_data.get("typed_content_text", ""),
        "content_link": user_data.get("typed_content_link", ""),
        "remove_content_image": user_data.get("remove_content_image", ""),
    }
    files = {}
    content_image = user_data.get("sent_content_image", None)
    if content_image is not None:
        files = {"content_image": content_image}

    response = await putch_button_content(button_id, data, files)
    await message_button_response(response, message, state)
    await cancel_and_return_to_admin_panel(message, state)