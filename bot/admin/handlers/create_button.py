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
from bot import bot
import requests

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup)
from .base import cancel_and_return_to_admin_panel, base_reply_markup
from crud import add_child_button, get_button_image
import os
import httpx


import os.path

API_URL = os.getenv('API_URL')
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


def parse_entities(message: Message) -> str:
    text = message.text
    if not text:
        return ""
    
    formatted_text = text
    for entity in message.entities:
        entity_text = text[entity.offset:entity.offset + entity.length]
        if entity.type == 'bold':
            formatted_text = formatted_text.replace(entity_text, hbold(entity_text))
        elif entity.type == 'italic':
            formatted_text = formatted_text.replace(entity_text, hitalic(entity_text))
        elif entity.type == 'text_link':
            formatted_text = formatted_text.replace(entity_text, hlink(entity_text, entity.url))
        # Можно добавить другие типы форматирования по необходимости

    return formatted_text


@router.message(CreateButton.typing_content_text)
async def content_text_typed(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await cancel_and_return_to_admin_panel(message, state)
        return
    if message.text != "Пропустить":
        await state.update_data(typed_content_text=message.html_text)
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
        photo_id = message.photo[-1].file_id
        photo_path_ = await bot.get_file(photo_id)
        photo_path = photo_path_.file_path

        photo_bytes = BytesIO()
        await bot.download_file(photo_path, photo_bytes)
        photo_bytes.seek(0)

        # file_ids = []
        # with open(file_stream, "rb") as image_from_buffer:
        #     result = await message.answer_photo(
        #         BufferedInputFile(
        #             image_from_buffer.read(),
        #             filename="image from buffer.jpg"
        #         ),
        #         caption="Изображение из буфера"
        #     )
        #     file_ids.append(result.photo[-1].file_id)
        # await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))
        await state.update_data(sent_content_image=photo_bytes)

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
            # f"<b>{user_data.get('typed_content_text', '')}</b>\n"
            f"{user_data.get('typed_content_text', '')}\n"
            f"Линк кнопки: <b>{user_data.get('typed_content_link', '')}</b>\n"
            f"Изображение:"
        ),
        reply_markup=new_reply_markup,
        parse_mode=ParseMode.HTML,
    )
    if "sent_content_image" in user_data:
        await message.answer_photo(photo=photo_id)
        # # тест, что изображение сохранилось в бинарном формате (работает)
        # with open("image.jpg", "wb") as f:
        #     f.write(user_data['sent_content_image'].read())
        # # и что бинарное изображение принимает и отображает телега (не получилось)
        # photo_bytes = user_data['sent_content_image']
        # photo_bytes.seek(0)
        # photo = InputFile(photo_bytes, filename="image.jpg")
        # await message.answer_photo(photo=photo)

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

    # await message.answer(
    #     text=(
    #         f"Успешно создал кнопку:\n"
    #         f"Айди кнопки: <b>{button['id']}</b>\n"
    #         f"Текст на кнопке: <b>{button['label']}</b>\n"
    #         f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
    #         f"Текст сообщения над кнопкой:\n{button['content_text']}\n"
    #         f"Линк кнопки: <b>{button['content_link']}</b>\n"
    #         # f"Изображение (путь): <b>{button['content_image']}</b>"
    #         f"Изображение:"
    #     ),
    #     parse_mode=ParseMode.HTML,
    # )
    # await message.answer_photo(
    #     URLInputFile(f"{API_URL}{button['content_image']}"))

    text = (
        f"Успешно создал кнопку:\n"
        f"Айди кнопки-родителя: <b>{button['parent_id']}</b>\n"
        f"Айди кнопки: <b>{button['id']}</b>\n"
        f"Текст на кнопке: <b>{button['label']}</b>\n"
        f"Текст сообщения над кнопкой:\n{button['content_text']}\n"
        f"Линк кнопки: <b>{button['content_link']}</b>\n"
    )
    # сломается, если нет изображения
    await message.answer_photo(
        photo=URLInputFile(f"{API_URL}{button['content_image']}"),
        caption=text,
        parse_mode=ParseMode.HTML
    )

    await cancel_and_return_to_admin_panel(message, state)


@router.message(F.photo)
async def photo_msg(message: Message):
    file_id = message.photo[-1].file_id
    file_path_ = await bot.get_file(file_id)
    file_path = file_path_.file_path
    await bot.download_file(file_path, "1.jpg")

    # Загружаем файл в BytesIO (чтобы сохранить его в памяти)
    file_stream = BytesIO()
    await bot.download_file(file_path, file_stream)
    file_stream.seek(0)  # Сбрасываем указатель в начало потока, чтобы его можно было прочитать

    # Создаем файл на диске и записываем в него данные из stream
    with open("2.jpg", "wb") as f:  # "wb" для записи в двоичном формате
        f.write(file_stream.read())

    await message.answer("Это точно какое-то изображение!")
    # await message.answer_photo(photo="1.jpg")
    # await response = requests.get('http://127.0.0.1/bot_menu/41/get-image-file')

    # async with httpx.AsyncClient() as client:
    #     response = await client.get('http://127.0.0.1/bot_menu/41/get-image-file')
    # image_stream = io.BytesIO(response.content)
    # image_stream.seek(0)
    # await message.answer_photo(photo=image_stream)

    # await message.answer_photo(photo="http://127.0.0.1/bot_menu/41/get-image-file")
    
    image_from_url = URLInputFile("http://127.0.0.1/files/photo_2024-07-26_02-52-14.jpg_1728851312.jpg")
    await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )

    image_from_url = URLInputFile("http://127.0.0.1/files/upload_1728847314")
    await message.answer_photo(
        image_from_url,
        caption="Изображение без формата по ссылке"
    )

    # await message.answer_photo(photo="http://127.0.0.1/files/photo_2024-07-26_02-52-14.jpg_1728851312.jpg")
    # await message.answer_photo(photo="http://127.0.0.1/files/upload_1728847314.jpg")
