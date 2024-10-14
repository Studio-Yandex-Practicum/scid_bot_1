from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext

from api.api_service import get_main_menu_button
from utils.state import NavigationState
from utils.user_content import generate_content, return_message

router = Router()


@router.message(F.text == "/start")
async def start_command(message: types.Message, state: FSMContext, bot: Bot):
    """Обработка команды /start."""
    main_button = await get_main_menu_button()
    await return_message(
        await generate_content(main_button['id']),
        message,
        state
    )
    await state.set_state(NavigationState.at_menu)

