from aiohttp import ClientSession

from core.config import settings

async def post_api_data(
    endpoint: str,
    data: dict = None,
    headers: dict = {},
    params: dict = {},
    json: dict = None
):
    async with ClientSession() as session:
        async with session.post(
            f"{settings.api.base_url}/{endpoint}",
            data=data,
            headers=headers,
            params=params,
            json=json
        ) as response:
            return await response.json()


async def get_api_data(
    endpoint: str,
    params: dict = {},
    headers: dict = {}
):
    async with ClientSession() as session:
        async with session.get(
            f'{settings.api.base_url}/{endpoint}',
            headers=headers,
            params=params
        ) as response:
            return await response.json()


async def patch_api_data(
    endpoint: str,
    data: dict = {},
    headers: dict = {},
    params: dict = {}
):
    async with ClientSession() as session:
        async with session.patch(
            f'{settings.api.base_url}/{endpoint}',
            data=data,
            headers=headers,
            params=params
        ) as response:
            return await response.json()


async def delete_api_data(
    endpoint: str,
    data: dict = {},
    headers: dict = {},
    params: dict = {}
):
    async with ClientSession() as session:
        async with session.delete(
            f'{settings.api.base_url}/{endpoint}',
            data=data,
            headers=headers,
            params=params
        ) as response:
            return await response.json()
