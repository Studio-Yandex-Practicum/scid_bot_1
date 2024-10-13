from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup)

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
                "callback_data": "get_button_subs",
            },
            {
                "text": "Изменить контент кнопки",
                "callback_data": "putch_button_content",
            },
            {
                "text": "Изменить родителя кнопки",
                "callback_data": "putch_button_parent",
            },
            {"text": "Удалить кнопку", "callback_data": "delete_button"},
        ]
    },
}


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
