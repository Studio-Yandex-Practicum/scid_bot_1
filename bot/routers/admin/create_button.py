from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from core.config import settings

from routers.crud import add_child_button, get_button_content
from routers.tree_commands import send_tree

from .base import (base_reply_markup, cancel_and_return_to_admin_panel,
                   handle_photo_upload, message_button_response,
                   not_required_reply_markup, validate_response)

API_URL = settings.api.base_url
router = Router()


class CreateButton(StatesGroup):
    typing_button_name = State()
    typing_parent_id = State()
    typing_content_text = State()
    typing_content_link = State()
    adding_content_image = State()
    submiting_button = State()


@router.callback_query(F.data == "post_button")
async def handle_post_button(callback: types.CallbackQuery, state: FSMContext):
    await send_tree(callback.message)
    await callback.message.answer(
        text="Введите айди кнопки-родителя:", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(CreateButton.typing_parent_id)


@router.message(CreateButton.typing_parent_id)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if not message.text.isdigit():
        await message.answer("Введите число")
        return
    response = await get_button_content(int(message.text))
    if not await validate_response(response, message, state):
        return
    await state.update_data(typed_parent_id=message.text)
    await message.answer(
        text="Теперь введите название новой кнопки",
        reply_markup=base_reply_markup,
    )
    await state.set_state(CreateButton.typing_button_name)


@router.message(CreateButton.typing_button_name)
async def parent_id_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_name=message.text)
    await message.answer(
        text="Теперь введите текст сообщения над кнопкой (можно пропустить):",
        reply_markup=not_required_reply_markup,
    )
    await state.set_state(CreateButton.typing_content_text)


@router.message(CreateButton.typing_content_text)
async def content_text_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        await state.update_data(typed_content_text=message.html_text)
    await message.answer(
        text="Теперь отправьте линк кнопки (можно пропустить):",
        reply_markup=not_required_reply_markup,
    )
    await state.set_state(CreateButton.typing_content_link)


@router.message(CreateButton.typing_content_link)
async def content_link_sent(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        await state.update_data(typed_content_link=message.text)
    await message.answer(
        text="Теперь отправьте изображение, "
        "которое будет над кнопкой (можно пропустить):",
        reply_markup=not_required_reply_markup,
    )
    await state.set_state(CreateButton.adding_content_image)


@router.message(CreateButton.adding_content_image)
async def content_image_sent(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        photo_id = await handle_photo_upload(message, state)
    user_data = await state.get_data()
    new_reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Создать кнопку")]]
        + base_reply_markup.keyboard,
        resize_keyboard=True,
    )

    await message.answer(
        text=(
            f"Кнопка почти готова, осталось подтвердить:\n"
            f"Текст на кнопке: <b>{user_data['typed_name']}</b>\n"
            f"Айди кнопки-родителя: <b>{user_data['typed_parent_id']}</b>\n"
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

    await state.set_state(CreateButton.submiting_button)


@router.message(CreateButton.submiting_button)
async def button_submited(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    user_data = await state.get_data()
    label = user_data["typed_name"]
    parent_id = user_data["typed_parent_id"]
    content_text = user_data.get("typed_content_text", "")
    content_link = user_data.get("typed_content_link", "")
    content_image = user_data.get("sent_content_image", None)
    auth_token = user_data.get("auth_token", "")

    print(content_image)

    response = await add_child_button(
        label, parent_id, content_text, content_link, content_image, auth_token
    )
    if await message_button_response(response, message, state):
        await cancel_and_return_to_admin_panel(message, state)
