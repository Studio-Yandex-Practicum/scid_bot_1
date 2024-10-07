import os
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
import aiohttp

# Загрузка переменных окружения
load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
API_URL = os.getenv("API_URL")
JWT_TOKEN = os.getenv("JWT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)  # Изменено здесь
router = Router()

# FSM (состояния)


class ButtonStates(StatesGroup):
    choosing_action = State()
    entering_label = State()
    entering_content_text = State()
    entering_content_image = State()
    entering_content_link = State()
    choosing_parent_id = State()
    final_choice = State()

# Стартовая команда для редактирования


@router.message(Command("start_edit"))
async def start_edit(message: Message, state: FSMContext):
    # Показываем клавиатуру с вариантами
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Создать новую кнопку")],
        [KeyboardButton(text="Добавить кнопку к родительской")]
    ], resize_keyboard=True)

    await message.answer("Что вы хотите сделать?", reply_markup=keyboard)
    await state.set_state(ButtonStates.choosing_action)

# Обработка выбора действия


@router.message(ButtonStates.choosing_action)
async def handle_choosing_action(message: Message, state: FSMContext):
    if message.text == "Создать новую кнопку":
        await create_new_button(message, state)
    elif message.text == "Добавить кнопку к родительской":
        await add_to_existing_button(message, state)


async def create_new_button(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_URL}/bot_menu/get-main-menu-button"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    main_button_id = result.get("id")
                else:
                    await message.answer(
                        "Ошибка при добавлении кнопки."
                        f" Статус: {response.status}"
                    )
        except Exception as e:
            await message.answer(
                f"Произошла ошибка при обращении к FastAPI: {str(e)}"
            )
    # Устанавливаем родителя по умолчанию
    await state.update_data(parent_id=main_button_id)
    await message.answer("Введите label для новой кнопки (обязательно):")
    await state.set_state(ButtonStates.entering_label)


async def add_to_existing_button(message: Message, state: FSMContext):
    await message.answer("Введите ID родительской кнопки:")
    await state.set_state(ButtonStates.choosing_parent_id)

# Ввод parent_id


@router.message(ButtonStates.choosing_parent_id)
async def set_parent_id(message: Message, state: FSMContext):
    parent_id = int(message.text)
    await state.update_data(parent_id=parent_id)
    await message.answer("Введите label для новой кнопки (обязательно):")
    await state.set_state(ButtonStates.entering_label)

# Ввод label (обязательное поле)


@router.message(ButtonStates.entering_label)
async def set_label(message: Message, state: FSMContext):
    label = message.text
    await state.update_data(label=label)

    # Спрашиваем, хочет ли админ добавить текстовое содержание
    await message.answer("Введите content_text (или отправьте 'пропустить'):")
    await state.set_state(ButtonStates.entering_content_text)

# Пропуск или ввод content_text


@router.message(ButtonStates.entering_content_text)
async def set_content_text(message: Message, state: FSMContext):
    content_text = message.text if message.text.lower() != "пропустить" else ""
    await state.update_data(content_text=content_text)

    await message.answer("Введите content_image (или отправьте 'пропустить'):")
    await state.set_state(ButtonStates.entering_content_image)

# Пропуск или ввод content_image


@router.message(ButtonStates.entering_content_image)
async def set_content_image(message: Message, state: FSMContext):
    content_image = message.text if message.text.lower() != "пропустить" else ""
    await state.update_data(content_image=content_image)

    await message.answer("Введите content_link (или отправьте 'пропустить'):")
    await state.set_state(ButtonStates.entering_content_link)

# Пропуск или ввод content_link


@router.message(ButtonStates.entering_content_link)
async def set_content_link(message: Message, state: FSMContext):
    content_link = message.text if message.text.lower() != "пропустить" else ""
    await state.update_data(content_link=content_link)

    # Отправляем POST запрос на API
    await send_post_request(message, state)

# Отправка POST-запроса на API


async def send_post_request(message: Message, state: FSMContext):
    user_data = await state.get_data()
    parent_id = user_data.get('parent_id')
    label = user_data.get('label')
    content_text = user_data.get('content_text')
    content_image = user_data.get('content_image')
    content_link = user_data.get('content_link')

    form_data = aiohttp.FormData()
    form_data.add_field('label', label)
    form_data.add_field('content_text', content_text)
    form_data.add_field('content_image', content_image)
    form_data.add_field('content_link', content_link)
    form_data.add_field('parent_id', str(parent_id))
    print(JWT_TOKEN)
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/bot_menu/{parent_id}/add-child-button",
                data=form_data,
                headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    new_button_id = result.get("id")
                    await state.update_data(new_button_id=new_button_id)
                    # Передаем state здесь!
                    await show_choice_menu(message, new_button_id, state)
                else:
                    await message.answer(
                        "Ошибка при добавлении кнопки."
                        f" Статус: {response.status}"
                    )
        except Exception as e:
            await message.answer(
                f"Произошла ошибка при обращении к FastAPI: {str(e)}"
            )

# После добавления кнопки — выбор действия


# Добавляем state здесь!
async def show_choice_menu(message: Message,
                           new_button_id: int,
                           state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Создать дочернюю кнопку")],
        [KeyboardButton(text="Создать новую кнопку")]
    ], resize_keyboard=True)

    await message.answer(
        "Кнопка успешно добавлена!"
        f" ID: {new_button_id}\nЧто хотите сделать дальше?",
        reply_markup=keyboard
    )
    await state.set_state(ButtonStates.final_choice)  # Обновляем состояние

# Обработка выбора после добавления


@router.message(ButtonStates.final_choice)
async def handle_final_choice(message: Message, state: FSMContext):
    if message.text == "Создать дочернюю кнопку":
        await create_child_button(message, state)
    elif message.text == "Создать новую кнопку":
        await create_new_button_after(message, state)


async def create_child_button(message: Message, state: FSMContext):
    # Получаем ID родителя — это кнопка, которую только что создали
    user_data = await state.get_data()
    new_button_id = user_data.get("new_button_id")

    # Важно: устанавливаем новое состояние для добавления новой кнопки,
    # а не сразу отправляем запрос
    await state.update_data(parent_id=new_button_id)
    await message.answer(
        "Введите label для новой дочерней кнопки (обязательно):"
    )
    await state.set_state(ButtonStates.entering_label)


async def create_new_button_after(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_URL}/bot_menu/get-main-menu-button"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    main_button_id = result.get("id")
                else:
                    await message.answer(
                        "Ошибка при получении главной кнопки."
                        f" Статус: {response.status}"
                    )
        except Exception as e:
            await message.answer(
                f"Произошла ошибка при обращении к FastAPI: {str(e)}"
            )
    await state.update_data(parent_id=main_button_id)
    await message.answer("Введите label для новой кнопки (обязательно):")
    await state.set_state(ButtonStates.entering_label)

# Регистрация маршрутов
dp.include_router(router)

# Основная функция запуска бота


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
