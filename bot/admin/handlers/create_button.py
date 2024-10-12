from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup)
from .base import cancel_and_return_to_admin_panel, base_reply_markup
from crud import add_child_button

router = Router()


# FSM создать кнопку
class CreateButton(StatesGroup):
    typing_button_name = State()
    typing_parent_id = State()
    typing_content_text = State()
    typing_content_link = State()
    adding_content_image = State()
    submiting_button = State()


not_required_reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]]
    + base_reply_markup.keyboard,
    resize_keyboard=True,
)


@router.callback_query(F.data == "post_button")
async def handle_post_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите название новой кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(CreateButton.typing_button_name)


@router.message(CreateButton.typing_button_name)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_name=message.text)
    await message.answer(
        text="Теперь введите айди кнопки-родителя:",
        reply_markup=base_reply_markup,
    )
    await state.set_state(CreateButton.typing_parent_id)


@router.message(CreateButton.typing_parent_id)
async def parent_id_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    # if message.text == "Назад":
    #     await state.set_state(CreateButton.typing_button_name)
    #     await message.answer(
    #         text="Введите название новой кнопки",
    #         reply_markup=base_reply_markup
    #     )
    #     return
    await state.update_data(typed_parent_id=message.text)
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
        await state.update_data(typed_content_text=message.text)
    await message.answer(
        text="Теперь отправьте линк кнопки (можно пропустить):",  # где будет этот линк?
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
        photo = message.photo[-1].file_id
        await state.update_data(sent_content_image=photo)
    user_data = await state.get_data()
    new_reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Создать кнопку")]]
        + base_reply_markup.keyboard,
        resize_keyboard=True,
    )
    await message.answer(
        # await message.answer_photo(
        # photo=user_data['sent_content_image'],
        text=(
            f"Кнопка почти готова, осталось подтвердить:\n"
            f"Текст на кнопке: <b>{user_data['typed_name']}</b>\n"
            f"Айди кнопки-родителя: <b>{user_data['typed_parent_id']}</b>\n"
            f"Текст сообщения над кнопкой: "
            f"<b>{user_data.get('typed_content_text', '')}</b>\n"
            f"Линк кнопки: <b>{user_data.get('typed_content_link', '')}</b>\n"
            f"Изображение:"
        ),
        reply_markup=new_reply_markup,
        parse_mode=ParseMode.HTML,
    )
    if "sent_content_image" in user_data:
        await message.answer_photo(photo=photo)
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

    button = await add_child_button(
        label, parent_id, content_text, content_link, content_image
    )
    await message.answer(
        text=(
            f"Успешно создал кнопку:\n"
            f"Текст на кнпоке: <b>{button['label']}</b>\n"
            f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
            f"Текст сообщения над кнопкой: <b>{button['content_text']}</b>\n"
            f"Линк кнопки: <b>{button['content_link']}</b>\n"
            f"Изображение: <b>{button['content_image']}</b>"
        ),
        parse_mode=ParseMode.HTML,
    )
    await cancel_and_return_to_admin_panel(message, state)
