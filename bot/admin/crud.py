import os

import requests
from dotenv import load_dotenv
import httpx


load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_BOT_MENU_URL = os.getenv('API_BOT_MENU_URL')  # проставить


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
        print(content_image)
        files = {"content_image": content_image}
    else:
        files = {}
    async with httpx.AsyncClient() as client:
        response = await client.post(url,
                                     headers=headers,
                                     data=data,
                                     files=files)
    return response.json()


async def get_button_content(button_id):
    url = f'{API_BOT_MENU_URL}{button_id}/get-content'
    headers = {
        'accept': 'application/json',
    }
    # response = requests.get(url, headers=headers)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    # return response.json()
    return response
