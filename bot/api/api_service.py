import os
import aiohttp


# API_BASE_URL = os.getenv("API_BASE_URL")
API_BASE_URL="http://127.0.0.1"

async def get_main_menu_button():
    """Получить базовую кнопку."""
    url = f"{API_BASE_URL}/bot_menu/get-main-menu-button"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_button_content(button_id):
    """Получить контент кнопки по её ID."""
    url = f"{API_BASE_URL}/bot_menu/{button_id}/get-content"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_button_image(button_id):
    """Получить изображение кнопки (шифрованная строка)."""
    url = f"{API_BASE_URL}/bot_menu/{button_id}/get-image-file"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def get_child_buttons(button_id):
    """Получить дочерние кнопки по ID родителя."""
    url = f"{API_BASE_URL}/bot_menu/{button_id}/get-child-buttons"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
