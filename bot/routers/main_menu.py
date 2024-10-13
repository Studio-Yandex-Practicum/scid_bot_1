from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext

from api.api_service import get_main_menu_button
from utils.state import NavigationState
from utils.user_content import generate_content, return_message
from utils.menus import set_commands

router = Router()


@router.message(F.text == "/start")
async def start_command(message: types.Message, state: FSMContext, bot: Bot):
    """Обработка команды /start."""
    main_button = await get_main_menu_button()
    await set_commands(bot, message.from_user.id)
    await return_message(
        await generate_content(main_button['id']),
        message
    )
    await state.set_state(NavigationState.at_menu)

