import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram import Router
import asyncio
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()

# Начальное меню
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Нажми меня", callback_data="change_text")
    keyboard.add(button)
    await message.answer("Привет! Нажмите на кнопку.", reply_markup=keyboard)

# # Обработка нажатия на кнопку
# @router.callback_query(F.data == 'change_text')
# async def change_button_text(callback_query: types.CallbackQuery):
#     keyboard = types.InlineKeyboardMarkup()
#     new_button = types.InlineKeyboardButton("Текст изменён", callback_data="new_action")
#     keyboard.add(new_button)
    
#     # Редактируем сообщение с новой кнопкой
#     await callback_query.message.edit_text("Кнопка обновлена!", reply_markup=keyboard)
#     await callback_query.answer()  # Подтверждаем, что колбек обработан

dp.include_router(router)

# Основная функция запуска бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
