import os
import httpx
import aiohttp
from aiohttp import ClientError
from dotenv import load_dotenv
import functools
from core.config import settings


load_dotenv()

# AUTH_TOKEN = os.getenv("AUTH_TOKEN")
# API_BOT_MENU_URL = os.getenv("API_BOT_MENU_URL")
API_TOKEN = settings.app.token
API_URL = settings.api.base_url
# API_BOT_MENU_URL = 'http://127.0.0.1/bot_menu/'
# API_BOT_MENU_URL = 'http://localhost/bot_menu/'
# API_BOT_MENU_URL = 'http://fastapi_app:8000/bot_menu/'  # тоже работает

# API_BOT_MENU_URL = 'http://nginx/bot_menu/'
API_BOT_MENU_URL = f"{API_URL}/bot_menu/"

# API_TG_AUTH_URL = "http://nginx/auth/get_user-jwf-by-tg-id"
API_TG_AUTH_URL = f"{API_URL}/auth/get_user-jwf-by-tg-id"


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
    # print("dddddddddddddddddddddddddddddddddddddddddddd")
    url = f"{API_BOT_MENU_URL}{button_id}/get-content"
    headers = {
        "accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        print(url)
        response = await client.get(url, headers=headers)
        # print("dddddddddddddddddddddddddddddddddddddddddddd")
    print(response)
    return response


# @handle_http_errors
# async def get_button_content(button_id):
#     url = f"{API_BOT_MENU_URL}{button_id}/get-content"
#     headers = {
#         "accept": "application/json",
#     }

#     async with aiohttp.ClientSession() as session:
#         try:
#             print(url)
#             async with session.get(url, headers=headers) as response:
#                 print("dddddddddddddddddddddddddddddddddddddddddddd")
#                 response_data = await response.text()
#                 print(response_data)
#                 return response_data
#         except ClientError as e:
#             print(f"Request failed: {e}")
#             raise


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


# может передать сразу params?
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


# может лучше передать переменные со значениями, как в функции выше
# а внутри уже собрать в headers?
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


# handle_http_errors
# async def get_user_jwf_by_tg_id(user_id):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(
#             API_AUTH_URL, 
#             headers={
#                 "accept": "application/json", 
#                 "Content-Type": "application/x-www-form-urlencoded"
#             }, 
#             data={"tg_id": user_id}  # Передаем tg_id в формате form-data
#         ) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 auth_token = data.get("token")
                
#                 # Сохраняем токен в state
#                 await state.update_data(AUTH_TOKEN=auth_token)
                
#                 await message.answer("Вы успешно авторизованы.")
#             else:
#                 await message.answer("Ошибка авторизации.")


@handle_http_errors
async def get_user_jwf_by_tg_id(tg_user_id):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "tg_id": tg_user_id
    }
    # print('ооооооооооооооооооо')
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_TG_AUTH_URL,
            headers=headers,
            data=data)
    # print('aaaaaaaaaaaaaaaaaaaaaaaa')

    return response
