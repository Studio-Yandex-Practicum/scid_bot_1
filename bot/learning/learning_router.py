import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram import Router
import asyncio
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)
router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку, чтобы получить приветствие.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Поздороваться", callback_data="greet"
                    )
                ]
            ]
        ),
    )


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
