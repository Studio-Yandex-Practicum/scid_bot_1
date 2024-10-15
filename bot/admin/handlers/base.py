import os
import os.path
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup,
                           URLInputFile)

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