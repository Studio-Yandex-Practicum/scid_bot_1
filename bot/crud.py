import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")


async def add_child_button(name, parent_id):
    url = f"http://127.0.0.1/bot_menu/{int(parent_id)}/add-child-button"
    headers = {
        "accept": "application/json",
        "Authorization": AUTH_TOKEN,
    }
    data = {"label": name, "content_text": "string", "content_link": "string"}
    # files = {'content_image': open('/path/to/your/image.png', 'rb')}
    response = requests.post(url, headers=headers, data=data)
    # response = requests.post(url, headers=headers, data=data, files=files)
    return response.json()
