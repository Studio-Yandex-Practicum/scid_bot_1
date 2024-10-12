import os

import aiofiles
import aiofiles.os
import aiofiles.ospath
import yaml
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

import core.base
from core.config import settings


async def copy_image_files(images_dir: str):
    for file in await aiofiles.os.listdir(images_dir):
        old_file_path = os.path.join(images_dir, file)
        new_file_path = os.path.join(settings.app.base_dir_for_files, file)
        if not await aiofiles.ospath.exists(new_file_path):
            async with aiofiles.open(old_file_path, 'rb') as fd_src:
                async with aiofiles.open(new_file_path, 'wb') as fd_dst:
                    while True:
                        chunk = await fd_src.read(1024)
                        if not chunk:
                            break
                        await fd_dst.write(chunk)
    print('Файлы фикстур скопированы')


async def reset_sequences(table_name: str, session: AsyncSession):
    result = await session.execute(text(f'SELECT MAX(id) FROM {table_name}'))
    max_id = result.scalar() or 0
    await session.execute(
        text(
            f"SELECT SETVAL(pg_get_serial_sequence(:table_name, :id_column), "
            f":new_id)"
        ).bindparams(table_name=table_name, id_column="id", new_id=max_id + 1)
    )
    await session.commit()


async def load_yaml(file_path: str) -> dict:
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        content = await file.read()
        data = yaml.safe_load(content)
    return data


async def insert_fixtures_to_db(data: dict, session: AsyncSession):
    for model_str in data:
        model = getattr(core.base, model_str)
        for entry in data[model_str]:
            obj = await session.get(model, entry["id"])
            if obj is None:
                session.add(model(**entry))
        await session.commit()
        await reset_sequences(model_str, session)
    print("Фикстуры загружены")


async def load_fixtures(
    file_path: str, images_dir: str, session: AsyncSession
):
    data = await load_yaml(file_path)
    await insert_fixtures_to_db(data, session)
    await copy_image_files(images_dir)
