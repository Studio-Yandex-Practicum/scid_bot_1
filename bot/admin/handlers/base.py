import os
import os.path
from io import BytesIO
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup,
                           URLInputFile)
from admin_bot import bot

API_URL = os.getenv("API_URL")
router = Router()

# корневое инлайн меню админки
admin_start_keyboard_structure = {
    "admin_block_start_message": "Разделы админки:",
    "main_menu": {
        "buttons": [
            {"text": "Создать кнопку", "callback_data": "post_button"},
            {
                "text": "Получить контент кнопки",
                "callback_data": "get_button_content",
            },
            {
                "text": "Получить все дочерние кнопки",
                "callback_data": "get_child_buttons",
            },
            {
                "text": "Изменить контент кнопки",
                "callback_data": "putch_button_content",
            },
            {
                "text": "Изменить родителя кнопки",
                "callback_data": "putch_button_parent",
            },
            {
                "text": "Удалить кнопку",
                "callback_data": "del_button_with_children",
            },
        ]
    },
}


# нижняя кнопка Отмена
base_reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
)


# нижние кнопки Отмена + Пропустить
not_required_reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]]
    + base_reply_markup.keyboard,
    resize_keyboard=True,
)


def generate_main_menu(buttons_structure):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button["text"], callback_data=button["callback_data"]
                )
            ]
            for button in buttons_structure["main_menu"]["buttons"]
        ]
    )
    return keyboard


@router.message(Command(commands=["admin"]))
async def show_base_admin_panel(message: types.Message):
    await message.answer(
        admin_start_keyboard_structure["admin_block_start_message"],
        reply_markup=generate_main_menu(admin_start_keyboard_structure),
    )


async def cancel_and_return_to_admin_panel(
    message: Message, state: FSMContext
):
    await state.clear()
    await message.answer(
        "Возвращаюсь в основное меню", reply_markup=types.ReplyKeyboardRemove()
    )
    await show_base_admin_panel(message)


# async def update_field_or_cancel_or_skip(message: Message, state: FSMContext, update_field: str = None):
#     if message.text == "Отмена":
#         await cancel_and_return_to_admin_panel(message, state)
#         return True  # Возвращаем True, чтобы выйти из основной функции
#     if message.text != "Пропустить" and update_field:
#         await state.update_data({update_field: message.text})
#     return False


async def show_button(button, message):
    text = (
        f"Успешно создал кнопку:\n"
        f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
        f"Айди кнопки: <b>{button['id']}</b>\n"
        f"Текст на кнопке: <b>{button['label']}</b>\n"
        f"Текст сообщения над кнопкой:\n{button['content_text']}\n"
        f"Линк кнопки: <b>{button['content_link']}</b>\n"
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)
    if button["content_image"] is not None:
        await message.answer_photo(
            photo=URLInputFile(f"{API_URL}{button['content_image']}"),
            caption=text,
            parse_mode=ParseMode.HTML,
        )


async def handle_photo_upload(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    photo_path_ = await bot.get_file(photo_id)
    photo_path = photo_path_.file_path

    photo_bytes = BytesIO()
    await bot.download_file(photo_path, photo_bytes)
    photo_bytes.seek(0)

    await state.update_data(sent_content_image=photo_bytes)
    return photo_id


# async def photo_from_message_to_obj(message: Message):
#     photo_id = message.photo[-1].file_id
#     photo_path_ = await bot.get_file(photo_id)
#     photo_path = photo_path_.file_path

#     photo_bytes = BytesIO()
#     await bot.download_file(photo_path, photo_bytes)
#     photo_bytes.seek(0)
#     return photo_bytes
