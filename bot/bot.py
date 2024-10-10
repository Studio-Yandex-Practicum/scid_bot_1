import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from dotenv import load_dotenv
import asyncio

# Загрузка переменных окружения из .env файла
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определение ID администраторов
ADMIN_IDS = [
    123456789,
    225735315,
]  # Замените на реальные Telegram ID администраторов

# Структура кнопок и сообщений
buttons_structure = {
    "admin_block_start_message": "Разделы админки:",
    "main_menu": {
        "buttons": [
            {"text": "Создать кнопку", "callback_data": "create_button"},
            {
                "text": "Получить контент кнопки",
                "callback_data": "get_button_content",
            },
            {
                "text": "Получить все дочерние кнопки",
                "callback_data": "get_button_subs",
            },
        ]
    },
}

# Простое хранилище для кнопок (ключ: callback_data, значение: текст кнопки)
buttons_storage = {}


# Определение состояний для создания кнопки
class CreateButtonStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_callback = State()


# Генерация клавиатуры на основе структуры
def generate_main_menu():
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


# Функция для проверки, является ли пользователь администратором
def is_admin(user_id):
    return user_id in ADMIN_IDS


# Хэндлер на команду /start
@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer(
            buttons_structure["admin_block_start_message"],
            reply_markup=generate_main_menu(),
        )
    else:
        await message.answer("У вас нет доступа к этому боту.")


# Хэндлер нажатий на кнопки
@dp.callback_query(F.data)
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data

    if not is_admin(user_id):
        await callback.answer(
            "У вас нет доступа к этим функциям.", show_alert=True
        )
        return

    if data == "create_button":
        await callback.message.answer("Введите текст для новой кнопки:")
        await state.set_state(CreateButtonStates.waiting_for_text)
    elif data == "get_button_content":
        await callback.message.answer(
            "Введите `callback_data` кнопки, контент которой хотите получить:"
        )
        await state.set_state(CreateButtonStates.waiting_for_callback)
    elif data == "get_button_subs":
        if buttons_storage:
            buttons_list = "\n".join(
                [
                    f"Callback Data: {key}, Text: {value}"
                    for key, value in buttons_storage.items()
                ]
            )
            await callback.message.answer(
                f"Все дочерние кнопки:\n{buttons_list}"
            )
        else:
            await callback.message.answer("Дочерних кнопок пока нет.")
    else:
        await callback.message.answer("Неизвестная команда.")


# Хэндлер для получения текста новой кнопки
@dp.message(CreateButtonStates.waiting_for_text)
async def process_button_text(message: types.Message, state: FSMContext):
    button_text = message.text.strip()
    if not button_text:
        await message.answer(
            "Текст кнопки не может быть пустым. Введите текст для новой кнопки:"
        )
        return
    await state.update_data(button_text=button_text)
    await message.answer("Введите `callback_data` для этой кнопки:")
    await state.set_state(CreateButtonStates.waiting_for_callback)


# Хэндлер для получения callback_data новой кнопки
@dp.message(CreateButtonStates.waiting_for_callback)
async def process_button_callback(message: types.Message, state: FSMContext):
    callback_data = message.text.strip()
    user_data = await state.get_data()
    button_text = user_data.get("button_text")

    if not callback_data:
        await message.answer(
            "`callback_data` не может быть пустым. Введите `callback_data` для этой кнопки:"
        )
        return

    if callback_data in buttons_storage:
        await message.answer(
            "Такая `callback_data` уже существует. Попробуйте снова."
        )
        await state.clear()
        return

    # Сохранение новой кнопки в хранилище
    buttons_storage[callback_data] = button_text
    await message.answer(
        f"Кнопка создана:\nText: {button_text}\nCallback Data: {callback_data}"
    )
    await state.clear()

    # Обновление главного меню (по желанию можно добавить новые кнопки)
    # В данном примере новые кнопки сохраняются в buttons_storage и не добавляются в главное меню автоматически


# Обработка всех остальных сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(
        "Пожалуйста, используйте кнопки для взаимодействия с ботом."
    )


# Функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
