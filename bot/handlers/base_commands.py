from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils import markdown

from keyboards.common_keyboards import (
    get_start_keyboard,
)

# Cоздание маршрутизатора
# __name__ - для идентификации в логировании
router = Router(name=__name__)


# Обработка команды /start
@router.message(CommandStart())
async def handle_command_code(message: types.Message):
    await message.answer(
        text=f"Привет, {markdown.hbold(message.from_user.full_name)}!\nСпасибо, что установили наш бот!\n\nФункционал нашего бота:\n- Первое\n- Второе\n- Третье",
        parse_mode=ParseMode.HTML,
        # Ответ который отправил еще и клавиатуру
        reply_markup=get_start_keyboard(),
    )
