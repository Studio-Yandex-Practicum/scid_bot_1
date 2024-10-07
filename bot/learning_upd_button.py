import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram import Router
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создайте экземпляр Router
router = Router()

# Начальное меню
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    edit_button = types.InlineKeyboardButton("Изменить текст", callback_data="edit_button")
    keyboard.add(edit_button)
    await message.answer("Привет! Нажмите кнопку ниже, чтобы изменить текст.", reply_markup=keyboard)

# Обработка нажатия на кнопку
@router.callback_query(F.data == 'edit_button')
async def process_edit_button(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    new_button = types.InlineKeyboardButton("Текст изменен", callback_data="new_text")
    keyboard.add(new_button)

    await callback_query.message.edit_text("Текст кнопки изменился!", reply_markup=keyboard)

# Регистрируем маршрутизатор в диспетчере
dp.include_router(router)

# Основная функция запуска бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
