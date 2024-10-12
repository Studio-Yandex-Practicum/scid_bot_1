from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from api.api_service import get_main_menu_button, get_child_buttons
from keyboards.inline_keyboards import create_menu_keyboard
from utils.state import NavigationState

router = Router()

@router.message(F.text == "/start")
async def start_command(message: types.Message, state: FSMContext):
    """Обработка команды /start."""
    main_button = await get_main_menu_button()
    child_buttons = await get_child_buttons(main_button['id'])

    keyboard = create_menu_keyboard(child_buttons)
    await message.answer(main_button['label'], reply_markup=keyboard)

    await state.set_state(NavigationState.at_menu)

