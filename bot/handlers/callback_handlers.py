from aiogram import Router, types
from bot.handlers.handlers import (
    handle_menu_get_content,
    handle_menu_get_main_menu_button,
    handle_menu_get_child_buttons
)
from bot.keyboards.common_keyboards import inline_menu

router = Router()

# Хендлер для обработки нажатий на кнопки
@router.callback_query()
async def handle_button_click(callback_query: types.CallbackQuery):
    # Извлекаем данные из callback_data
    button_id, parent_id = callback_query.data.split(',')

    # Если это корневая кнопка (переход в начало)
    if button_id == '1':
        # Загрузить корневое меню
        child_buttons = await handle_menu_get_main_menu_button()
    else:
        # Получаем дочерние кнопки для текущего ID
        child_buttons = await handle_menu_get_child_buttons(button_id)

    # Если есть дочерние кнопки, показываем их
    if child_buttons:
        # Вызов функции inline_menu для создания клавиатуры
        keyboard = await inline_menu(child_buttons, start_id=1)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        # Если дочерних кнопок нет, показываем контент
        content = await handle_menu_get_content(button_id)
        if content:
            await callback_query.message.edit_text(f"Контент: {content.get('text')}")
        else:
            await callback_query.message.edit_text("Контент отсутствует.")

    await callback_query.answer()
