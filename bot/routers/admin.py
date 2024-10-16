from aiogram import Bot, Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from api.api_service import add_child_button, get_button_content
from keyboards.admin import (
    add_create_button_to_menu,
    BASE_REPLY_MARKUP,
    generate_main_menu,
    NOT_REQUIRED_REPLY_MARKUP
)
from utils.admin import show_base_admin_panel
from utils.admin_state import CreateButton


router = Router()


async def cancel_and_return_to_admin_panel(
    message: Message, state: FSMContext
):
    await state.clear()
    await message.answer(
        "Возвращаюсь в основное меню", reply_markup=types.ReplyKeyboardRemove()
    )
    await show_base_admin_panel(message)


@router.message(F.text == "/admin")
async def start_command(message: types.Message, state: FSMContext, bot: Bot):
    """Обработка команды /admin."""
    await message.answer(
        "Админ-панель SCID_BOT_1",
        reply_markup=await generate_main_menu(),
    )


@router.callback_query(F.data == "post_button")
async def handle_post_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите название новой кнопки", reply_markup=BASE_REPLY_MARKUP
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
        reply_markup=BASE_REPLY_MARKUP,
    )
    await state.set_state(CreateButton.typing_parent_id)


@router.message(CreateButton.typing_parent_id)
async def parent_id_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_parent_id=message.text)
    await message.answer(
        text="Теперь введите текст сообщения над кнопкой (можно пропустить):",
        reply_markup=NOT_REQUIRED_REPLY_MARKUP,
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
        text="Теперь отправьте линк кнопки (можно пропустить):",
        reply_markup=NOT_REQUIRED_REPLY_MARKUP,
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
        reply_markup=NOT_REQUIRED_REPLY_MARKUP,
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
    await message.answer(
        text=(
            f"Кнопка почти готова, осталось подтвердить:\n"
            f"Текст на кнопке: <b>{user_data['typed_name']}</b>\n"
            f"Айди кнопки-родителя: <b>{user_data['typed_parent_id']}</b>\n"
            f"Текст сообщения над кнопкой: "
            f"<b>{user_data.get('typed_content_text', '')}</b>\n"
            f"Линк кнопки: <b>{user_data.get('typed_content_link', '')}</b>\n"
            f"Изображение:"
        ),
        reply_markup=await add_create_button_to_menu(),
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
    print(button)
    await message.answer(
        text=(
            f"Успешно создал кнопку:\n"
            f"Текст на кнопке: <b>{button['label']}</b>\n"
            f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
            f"Текст сообщения над кнопкой: <b>{button['content_text']}</b>\n"
            f"Линк кнопки: <b>{button['content_link']}</b>\n"
            f"Изображение: <b>{button['content_image']}</b>"
        ),
        parse_mode=ParseMode.HTML,
    )
    await cancel_and_return_to_admin_panel(message, state)


@router.callback_query(F.data == "get_button_content")
async def handle_get_button(callback: types.CallbackQuery, state: FSMContext):
    await send_tree(callback.message)
    await callback.message.answer(
        text="Введите айди кнопки", reply_markup=BASE_REPLY_MARKUP
    )
    await callback.answer()
    await state.set_state(CreateButton.typing_button_id)


@router.message(CreateButton.typing_button_id)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
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
