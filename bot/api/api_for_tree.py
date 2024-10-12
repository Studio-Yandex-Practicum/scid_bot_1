import aiohttp

API = 'http://127.0.0.1/bot_menu'


async def get_api_tree(button_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API}/{button_id}/get-child-buttons') as response:
            if response.status == 200:
                return await response.json()
            else:
                return None
