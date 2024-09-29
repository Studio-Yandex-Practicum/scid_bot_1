import aiofiles
import yaml

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import core.base


async def load_yaml(file_path: str) -> dict:
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
        content = await file.read()
        data = yaml.safe_load(content)
    return data


async def insert_fixtures_to_db(data: dict, session: AsyncSession):
    for model_str in data:
        model = getattr(core.base, model_str)
        for entry in data[model_str]:
            obj = await session.get(model, entry['id'])
            if obj is None:
                session.add(model(**entry))
    await session.commit()
    print('Фикстуры загружены')
    
        


async def load_fixtures(file_path: str, session: AsyncSession):
    data = await load_yaml(file_path)
    await insert_fixtures_to_db(data, session)
