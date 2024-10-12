import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, Message, ReplyKeyboardMarkup)
from crud import add_child_button
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN2")
if not API_TOKEN:
    raise ValueError(
        "Не найден токен бота. Пожалуйста,"
        "добавьте TELEGRAM_BOT_TOKEN в .env файл."
    )

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

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


@dp.message(Command(commands=["admin"]))
async def show_base_admin_panel(message: types.Message):
    await message.answer(
        admin_start_keyboard_structure["admin_block_start_message"],
        reply_markup=generate_main_menu(admin_start_keyboard_structure),
    )


# FSM создать кнопку
class CreateButton(StatesGroup):
    typing_button_name = State()
    typing_parent_id = State()
    typing_content_text = State()
    typing_content_link = State()
    adding_content_image = State()
    submiting_button = State()


base_reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        # [KeyboardButton(text="Назад")],
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,  # Опционально: делает клавиатуру компактной
    # one_time_keyboard=True  # Опционально: убирает клавиатуру после нажатия
)

not_required_reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]]
    + base_reply_markup.keyboard,
    resize_keyboard=True,
)


@dp.callback_query(F.data == "post_button")
async def handle_post_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите название новой кнопки", reply_markup=base_reply_markup
    )
    await callback.answer()
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(CreateButton.typing_button_name)


@dp.message(CreateButton.typing_button_name)
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


@dp.message(CreateButton.typing_parent_id)
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


@dp.message(CreateButton.typing_content_text)
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


@dp.message(CreateButton.typing_content_link)
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


@dp.message(CreateButton.adding_content_image)
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


@dp.message(CreateButton.submiting_button)
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


# отмена операции
async def cancel_and_return_to_admin_panel(
    message: Message, state: FSMContext
):
    await state.clear()
    await message.answer(
        "Возвращаюсь в основное меню", reply_markup=types.ReplyKeyboardRemove()
    )
    await show_base_admin_panel(message)


# проверка, что кнопка работает
@dp.callback_query(F.data == "get_button_content")
async def handle_get_button_content(callback: types.CallbackQuery):
    await callback.message.answer("ты нажал вторую кнопку")
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
