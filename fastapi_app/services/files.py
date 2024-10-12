import os
import time

import aiofiles
import aiofiles.os
import aiofiles.ospath
from core.config import settings
from fastapi import UploadFile


async def file_exists(file_path: str) -> bool:
    return await aiofiles.ospath.exists(file_path)


async def save_file(file: UploadFile) -> str:
    timestamp = int(time.time())
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{file.filename}_{timestamp}{file_extension}"
    file_path = os.path.join(settings.app.base_dir_for_files, unique_filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    return file_path


async def delete_file(file_path: str) -> str | None:
    if file_path is None:
        return None
    if await file_exists(file_path):
        await aiofiles.os.remove(file_path)
        return file_path
