import os
from typing import Any

from aiogram.types import CallbackQuery, FSInputFile

from api.api_service import get_button_content, get_child_buttons
from core.config import settings
from keyboards.inline_keyboards import create_menu_keyboard


async def generate_content(button_id: int) -> dict[str, Any]:
    content = await get_button_content(button_id)
    child_buttons = await get_child_buttons(button_id)
    keyboard = create_menu_keyboard(
        child_buttons, back_button=content['parent_id'] is not None
    )
    text_message = (
            f"<b>{content['label'] if content['label'] else ''}</b>\n\n"
            f"{content['content_text'] if content['content_text'] else ''}\n\n"
            f"{content['content_link'] if content['content_link'] else ''}\n\n"
        )
    image_path = os.path.normpath(
        os.path.join(settings.app.root_dir, content['content_image'])
    ) if content['content_image'] else None
    return {
        'keyboard': keyboard,
        'text': text_message,
        'image_path': image_path,
        'parent_id': content['parent_id']
    }


async def return_message(
    content: dict[str, Any],
    call: CallbackQuery
) -> Any:
    print(content['image_path'])
    if (
        content['image_path'] is None or
        not os.path.exists(content['image_path'])
    ):
        return await call.message.answer(
            text=content['text'],
            reply_markup=content['keyboard'],
            parse_mode="HTML"
        )
    image = FSInputFile(path=content['image_path'])
    return await call.message.answer_photo(
        caption=content['text'],
        photo=image,
        reply_markup=content['keyboard'],
        parse_mode="HTML"
    )
        