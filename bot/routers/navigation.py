from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from api.api_service import get_main_menu_button
from utils.state import NavigationState
from utils.user_content import generate_content, return_message

router = Router()

@router.callback_query(lambda c: c.data.isdigit())
async def navigate_to_button(
    call: types.CallbackQuery, state: FSMContext, bot: Bot
):
    """Обработка нажатия на кнопки с id."""
    button_id = int(call.data)
    content = await generate_content(button_id)
    await return_message(content, call, state)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

@router.callback_query(lambda c: c.data == "back")
async def go_back(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Возврат на уровень выше."""
    data = await state.get_data()
    current_button_id = data.get("current_button_id")
    parent_id = data.get("parent_id")
    if not current_button_id:
        await call.answer(
            "Ошибка: предыдущего меню не найдено.", show_alert=True
        )
        return
    content = await generate_content(parent_id)
    if not parent_id:
        await call.answer(
            "Вы уже находитесь в корневом меню.", show_alert=True
        )
        return
    await return_message(content, call, state)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@router.callback_query(lambda c: c.data == "main_menu")
async def go_to_main_menu(
    call: types.CallbackQuery, state: FSMContext, bot: Bot
):
    """Переход в главное меню."""
    main_button = await get_main_menu_button()
    content = await generate_content(main_button['id'])
    await return_message(content, call, state)
    await state.set_state(NavigationState.at_menu)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

