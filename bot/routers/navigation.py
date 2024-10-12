from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from api.api_service import get_button_content, get_button_image, get_child_buttons, get_main_menu_button
from utils.state import NavigationState
from keyboards.inline_keyboards import create_menu_keyboard

router = Router()

@router.callback_query(lambda c: c.data.isdigit())
async def navigate_to_button(call: types.CallbackQuery, state: FSMContext):
    """Обработка нажатия на кнопки с id."""
    button_id = int(call.data)  # Получаем ID нажатой кнопки
    content = await get_button_content(button_id)  # Запрашиваем контент этой кнопки
    child_buttons = await get_child_buttons(button_id)  # Получаем дочерние кнопки



    image = await get_button_image(button_id)
    

    # Создаем клавиатуру с кнопками
    keyboard = create_menu_keyboard(child_buttons, back_button=content['parent_id'] is not None)
    label = content['label']
    text = content['content_text']
    url = content['content_link']
    text_message = (
            f"<b>{label}</b>\n\n"
            f"{text}\n\n"
            f"{url}\n\n"
        )

    # Обновляем сообщение с новым контентом и клавиатурой
    await call.message.answer(
        text_message,
        #text=content['label'],
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    # Сохраняем текущее состояние в FSM
    await state.update_data(current_button_id=button_id)

@router.callback_query(lambda c: c.data == "back")
async def go_back(call: types.CallbackQuery, state: FSMContext):
    """Возврат на уровень выше."""
    data = await state.get_data()
    current_button_id = data.get("current_button_id")

    if not current_button_id:
        await call.answer("Ошибка: предыдущего меню не найдено.", show_alert=True)
        return

    # Получаем родительскую кнопку текущей кнопки
    content = await get_button_content(current_button_id)
    parent_id = content.get("parent_id")

    if not parent_id:
        await call.answer("Вы уже находитесь в корневом меню.", show_alert=True)
        return

    # Загружаем родительскую кнопку и её дочерние кнопки
    parent_content = await get_button_content(parent_id)
    child_buttons = await get_child_buttons(parent_id)

    # Обновляем сообщение с новым меню
    keyboard = create_menu_keyboard(child_buttons, back_button=parent_content['parent_id'] is not None)
    await call.message.edit_text(parent_content['label'], reply_markup=keyboard)

    # Обновляем текущее состояние
    await state.update_data(current_button_id=parent_id)

@router.callback_query(lambda c: c.data == "main_menu")
async def go_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    """Переход в главное меню."""
    main_button = await get_main_menu_button()
    child_buttons = await get_child_buttons(main_button['id'])

    # Обновляем сообщение с главным меню
    keyboard = create_menu_keyboard(child_buttons)
    await call.message.edit_text(main_button['label'], reply_markup=keyboard)

    # Сбрасываем состояние FSM на начальное
    await state.set_state(NavigationState.at_menu)
    await state.update_data(current_button_id=main_button['id'])

