from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase, ModelType


async def check_object_exist(
    object_id: int,
    crud_class: CRUDBase,
    error_text: str,
    session: AsyncSession,
) -> Optional[ModelType]:
    obj = await crud_class.get(obj_id=object_id, session=session)
    if obj is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error_text
        )
    return obj