import functools

import httpx
from core.config import settings
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = settings.app.token
API_URL = settings.api.base_url
API_BOT_MENU_URL = f"{API_URL}/bot_menu/"
API_TG_AUTH_URL = f"{API_URL}/auth/get_user-jwf-by-tg-id"


def handle_http_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            return response
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {e}")
            return None

    return wrapper


@handle_http_errors
async def add_child_button(
    label, parent_id, content_text, content_link, content_image, auth_token
):
    url = f"{API_BOT_MENU_URL}{int(parent_id)}/add-child-button"
    headers = {
        "accept": "application/json",
        "Authorization": auth_token,
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
    url = f"{API_BOT_MENU_URL}{button_id}/get-content"
    headers = {
        "accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        print(url)
        response = await client.get(url, headers=headers)
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
async def del_button_with_sub(button_id, auth_token):
    url = f"{API_BOT_MENU_URL}{button_id}"
    headers = {
        "accept": "application/json",
        "Authorization": auth_token,
    }
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
    return response


@handle_http_errors
async def putch_button_parent(button_id, new_parent_id, auth_token):
    url = f"{API_BOT_MENU_URL}{button_id}/change_parent"
    params = {
        "new_parent_id": new_parent_id,
    }
    headers = {
        "accept": "application/json",
        "Authorization": auth_token,
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, params=params)
    return response


@handle_http_errors
async def putch_button_content(button_id, data, files, auth_token):
    url = f"{API_BOT_MENU_URL}{int(button_id)}"
    headers = {
        "accept": "application/json",
        "Authorization": auth_token,
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url, headers=headers, data=data, files=files
        )
    return response


@handle_http_errors
async def get_user_jwf_by_tg_id(tg_user_id):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"tg_id": tg_user_id}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_TG_AUTH_URL, headers=headers, data=data
        )
    return response
