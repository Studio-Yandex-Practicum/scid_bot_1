from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hbold, hitalic, hlink
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.types import InputFile

# import requests
from io import BytesIO
import io

# from PIL import Image
# from bot import bot
import requests

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup)
from .base import cancel_and_return_to_admin_panel, base_reply_markup
from crud import putch_button_parent, get_button_content
import os
import httpx


import os.path

API_URL = os.getenv('API_URL')
router = Router()


# FSM создать кнопку
class PutchButtonParent(StatesGroup):
    typing_button_id = State()
    typed_new_parent_id = State()
    submiting_update_parent = State()


not_required_reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]]
    + base_reply_markup.keyboard,
    resize_keyboard=True,
)


@router.callback_query(F.data == "putch_button_parent")
async def handle_del_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите айди кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    await state.set_state(PutchButtonParent.typing_button_id)


@router.message(PutchButtonParent.typing_button_id)
async def name_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_button_id=message.text)
    await message.answer(
        text="Теперь введите айди новой кнопки-родителя:",
        reply_markup=base_reply_markup,
    )
    await state.set_state(PutchButtonParent.typed_new_parent_id)


@router.message(PutchButtonParent.typed_new_parent_id)
async def parent_id_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    await state.update_data(typed_new_parent_id=message.text)
    user_data = await state.get_data()
    new_reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔄 Обновить родительскую кнопку")]]
        + base_reply_markup.keyboard,
        resize_keyboard=True,
    )
    response = await get_button_content(user_data["typed_button_id"])
    button = response.json()
    await message.answer(
        text=(
            f"Обновляю?\n"
            f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
            f"Айди новой кнопки-родителя: <b>{user_data['typed_new_parent_id']}</b>\n"
        ),
        reply_markup=new_reply_markup,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(PutchButtonParent.submiting_update_parent)


@router.message(PutchButtonParent.submiting_update_parent)
async def button_submited(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    user_data = await state.get_data()
    button_id = user_data["typed_button_id"]
    new_parent_id = user_data["typed_new_parent_id"]

    response = await putch_button_parent(button_id, new_parent_id)
    print(response)
    button = response.json()
    print(button)
    await message.answer(
        text=(
            f"Успешно обновил родителя кнопки:\n"
            f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
            f"Айди кнопки: <b>{button['id']}</b>\n"
            f"Текст на кнопке: <b>{button['label']}</b>\n"
            f"Текст сообщения над кнопкой:\n{button['content_text']}\n"
            f"Линк кнопки: <b>{button['content_link']}</b>\n"
        ),
        parse_mode=ParseMode.HTML,
    )
    # text = (
    #     f"Успешно обновил родителя кнопки:\n"
    #     f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
    #     f"Айди кнопки: <b>{button['id']}</b>\n"
    #     f"Текст на кнопке: <b>{button['label']}</b>\n"
    #     f"Текст сообщения над кнопкой:\n{button['content_text']}\n"
    #     f"Линк кнопки: <b>{button['content_link']}</b>\n"
    # )
    # await message.answer_photo(
    #     photo=URLInputFile(f"{API_URL}{button['content_image']}"),
    #     caption=text,
    #     parse_mode=ParseMode.HTML
    # )

    await cancel_and_return_to_admin_panel(message, state)
