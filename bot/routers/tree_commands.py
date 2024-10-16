from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from api.api_service import get_main_menu_button
from utils.tree_utils import format_text, render_recursive


router = Router()


@router.message(Command(commands=["tree"]))
async def cmd_tree(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Посмотреть структуру")]
        ],
        resize_keyboard=True
    )
    await message.answer("Нажмите кнопку чтобы посмотреть структуру бота", reply_markup=keyboard)


@router.message(F.text == "Посмотреть структуру")
async def send_tree(message: Message):
    # Тут передаем id первой кнопки, лучше получать ее из API
    main_menu_button = await get_main_menu_button()
    tree_data = await render_recursive(main_menu_button["id"])
    if tree_data:
        result = format_text(tree_data)
        await message.answer(
            f"Главное меню ({main_menu_button['id']})\n{result}",
            parse_mode="HTML"
        )
    else:
        await message.answer("Не удалось получить данные от API.")
