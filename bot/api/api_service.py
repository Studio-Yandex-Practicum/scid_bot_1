from api.api_handlers import get_api_data, post_api_data


async def get_main_menu_button():
    """Получить базовую кнопку."""
    return await get_api_data(endpoint="bot_menu/get-main-menu-button")


async def get_button_content(button_id):
    """Получить контент кнопки по её ID."""
    return await get_api_data(endpoint=f"bot_menu/{button_id}/get-content")


async def get_button_image(button_id):
    """Получить изображение кнопки (шифрованная строка)."""
    return await get_api_data(endpoint=f"bot_menu/{button_id}/get-image-file")


async def get_child_buttons(button_id):
    """Получить дочерние кнопки по ID родителя."""
    return await get_api_data(
        endpoint=f"bot_menu/{button_id}/get-child-buttons"
    )


async def add_child_button(
    label, parent_id, content_text, content_link, content_image
):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3Mjg4ODA4Mjl9.raauyROylbUOBVOUL3f-kcQTusbqXP3Icwiljcs7Tlw",
    }
    data = {
        "label": label,
        "content_text": content_text,
        "content_link": content_link,
    }
    if content_image is not None:
        files = {"content_image": content_image}
    else:
        files = {}
    return await post_api_data(
            endpoint=f"bot_menu/{int(parent_id)}/add-child-button",
            data=data,
            headers=headers
        )