import os

import requests
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = os.getenv('API_URL')  # проставить


async def add_child_button(
    label, parent_id, content_text, content_link, content_image
):
    url = f"http://127.0.0.1/bot_menu/{int(parent_id)}/add-child-button"
    headers = {
        "accept": "application/json",
        "Authorization": AUTH_TOKEN,
    }
    data = {
        "label": label,
        "content_text": content_text,
        "content_link": content_link,
    }
    files = {"content_image": content_image}
    response = requests.post(url,
                             headers=headers,
                             data=data,
                             files=files)

    return response.json()


async def get_button_content(button_id):
    url = f'http://127.0.0.1/bot_menu/{button_id}/get-content'
    headers = {
        'accept': 'application/json',
    }
    response = requests.get(url, headers=headers)
    return response.json()
