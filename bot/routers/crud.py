import os
import httpx
from dotenv import load_dotenv
import functools
from core.config import settings


load_dotenv()

# AUTH_TOKEN = os.getenv("AUTH_TOKEN")
# API_BOT_MENU_URL = os.getenv("API_BOT_MENU_URL")
API_TOKEN = settings.app.token

API_URL = settings.api.base_url
API_BOT_MENU_URL = 'http://127.0.0.1/bot_menu/'


def handle_http_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            return response
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {e}")  # Можно заменить на логирование
            return None
    return wrapper


# может собрать все снаружи в headers?
@handle_http_errors
async def add_child_button(
    label, parent_id, content_text, content_link, content_image
):
    url = f"{API_BOT_MENU_URL}{int(parent_id)}/add-child-button"
    headers = {
        "accept": "application/json",
        "Authorization": AUTH_TOKEN,
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
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, data=data, files=files
        )
    return response


@handle_http_errors
async def get_button_content(button_id):
    print("dddddddddddddddddddddddddddddddddddddddddddd")
    url = f"{API_BOT_MENU_URL}{button_id}/get-content"
    headers = {
        "accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print("dddddddddddddddddddddddddddddddddddddddddddd")
        print(response)
        return response


@handle_http_errors
async def get_button_image(button_id):
    url = f"{API_BOT_MENU_URL}{button_id}/get-image-file"
    headers = {
        "accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    return response


@handle_http_errors
async def get_child_buttons(button_id):
    url = f"{API_BOT_MENU_URL}{button_id}/get-child-buttons"
    headers = {
        "accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    return response


@handle_http_errors
async def del_button_with_sub(button_id):
    url = f"{API_BOT_MENU_URL}{button_id}"
    headers = {
        "accept": "application/json",
        "Authorization": AUTH_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
    return response


# может передать сразу params?
@handle_http_errors
async def putch_button_parent(button_id, new_parent_id):
    url = f"{API_BOT_MENU_URL}{button_id}/change_parent"
    params = {
        "new_parent_id": new_parent_id,
    }
    headers = {
        "accept": "application/json",
        "Authorization": AUTH_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, params=params)
    return response


# может лучше передать переменные со значениями, как в функции выше
# а внутри уже собрать в headers?
@handle_http_errors
async def putch_button_content(button_id, data, files):
    url = f"{API_BOT_MENU_URL}{int(button_id)}"
    headers = {
        "accept": "application/json",
        "Authorization": AUTH_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url, headers=headers, data=data, files=files
        )
    return response
