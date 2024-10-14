from api.api_handlers import get_api_data, post_api_data

async def login_with_tg_id(tg_id: int) -> bool:
    await post_api_data(
        endpoint="auth/"
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