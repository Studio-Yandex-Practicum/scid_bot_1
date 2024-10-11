import os

from aiohttp import ClientSession
from dotenv import load_dotenv


load_dotenv()


API_URL = os.getenv('API_URL')


async def post_api_data(endpoint: str, data: dict):
    async with ClientSession() as session:
        async with session.post(
            API_URL, json={'endpoint': endpoint, 'data': data}
        ) as response:
            response_data = await response.json()
            return response_data['data']


async def get_api_data(endpoint: str, params: dict = None):
    async with ClientSession() as session:
        async with session.get(
            f'{API_URL}/{endpoint}', params=params
        ) as response:
            response_data = await response.json()
            return response_data['data']


async def patch_api_data(endpoint: str, data: dict):
    async with ClientSession() as session:
        async with session.patch(
            f'{API_URL}/{endpoint}', json=data
        ) as response:
            response_data = await response.json()
            return response_data['data']


async def delete_api_data(endpoint: str, data: dict = None):
    async with ClientSession() as session:
        async with session.delete(
            f'{API_URL}/{endpoint}', json=data
        ) as response:
            response_data = await response.json()
            return response_data['data']
