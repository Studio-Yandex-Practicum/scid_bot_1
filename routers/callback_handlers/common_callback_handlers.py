from aiogram import types
from aiogram import Router
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from keyboards.common_keyboards import ButtonCallback
from aiogram.types import CallbackQuery

# Cоздание маршрутизатора
# __name__ - для идентификации в логировании
router = Router(name=__name__)


# Тест пример
@router.callback_query(ButtonCallback.filter())
async def handle_callback(callback_query: types.CallbackQuery,
                          callback_data: ButtonCallback):
    # Сюда прийдет значение отправленное в value
    value = callback_data.value
    extra_info = callback_data.extra_info

    # Получаем текущую клавиатуру
    current_keyboard = callback_query.message.reply_markup.inline_keyboard

    # Создаем новую клавиатуру с подменой одной из кнопок
    # print(value)
    if value == "btn1":
        # Если нажата кнопка 1, меняем текст на кнопке 1
        new_button1 = InlineKeyboardButton(
            text="Rambler",
            callback_data=ButtonCallback(value="btn1",
                                         extra_info="updated").pack()
        )
        # Обновляем только первую кнопку, а остальные оставляем как есть
        current_keyboard[0][0] = new_button1

    # Обновляем клавиатуру в сообщении
    await callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(inline_keyboard=current_keyboard))


# Хендлер для команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Здравствуйте! Я ваш виртуальный помощник. Как я могу помочь вам сегодня?")

    # Получаем начальные кнопки с API
    buttons = await fetch_buttons_from_api(endpoint_id=1)
    keyboard = await inline_menu(buttons, columns=2)

    await message.answer("Выберите вариант:", reply_markup=keyboard)


# Хендлер для обработки нажатий на кнопки
@dp.callback_query_handler(lambda callback_query: ',' in callback_query.data)
async def process_callback(callback: CallbackQuery):
    button_id, parent_id = map(int, callback.data.split(','))

    # Запрашиваем новые кнопки на основе ID из API
    buttons = await fetch_buttons_from_api(endpoint_id=button_id)

    if buttons:
        keyboard = await inline_menu(buttons, columns=2, start_id=1)
        await callback.message.edit_text("Выберите следующий вариант:", reply_markup=keyboard)
    else:
        await callback.message.answer("К сожалению, информация недоступна.")


# Хендлер для возврата к начальному меню
@dp.callback_query_handler(lambda callback_query: callback_query.data.isdigit())
async def back_to_main_menu(callback: CallbackQuery):
    # Получаем начальные кнопки с API
    buttons = await fetch_buttons_from_api(endpoint_id=1)
    keyboard = await inline_menu(buttons, columns=2)

    await callback.message.edit_text("Возвращаемся обратно. Выберите один из них:",
                                     reply_markup=keyboard)
