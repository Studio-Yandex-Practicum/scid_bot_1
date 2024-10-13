import aiohttp

API_URL = 'http://127.0.0.1/bot_menu/get-main-menu-button'


# Асинхронная функция для получения данных с API
async def get_api_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                return await response.json()  # Получаем данные в формате JSON
            else:
                return None