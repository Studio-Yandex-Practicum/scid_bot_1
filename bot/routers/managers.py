from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.user_content import generate_content, return_message

router = Router()

@router.message(Command("manager"))
async def start_manager(
    call: types.Message, state: FSMContext, bot: Bot
):
    """Обработка команды /manager"""
    button_id = int(call.data)
    content = await generate_content(button_id)
    await return_message(content, call, state)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
