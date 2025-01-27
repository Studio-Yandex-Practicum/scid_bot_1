from typing import Any, Generic, Optional, TypeVar

from core.db import Base
from fastapi.encoders import jsonable_encoder
from models.user import User
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model) -> None:
        self.model = model

    async def _commit_and_refresh(self, obj: ModelType, session: AsyncSession):
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def _get_by_attribute(
        self, attribute: str, value: str, session: AsyncSession
    ) -> list[ModelType]:
        attr = getattr(self.model, attribute)
        db_obj = await session.execute(select(self.model).where(attr == value))
        return db_obj.scalars().all()

    async def _get_by_attributes(
        self,
        attributes: dict[str, Any],
        query_options: list[Any],
        session: AsyncSession,
    ) -> list[ModelType]:
        query = select(self.model)
        for attribute, value in attributes.items():
            attr = getattr(self.model, attribute)
            query = query.where(attr == value)
        for option in query_options:
            query = query.options(option)
        result = await session.execute(query)
        return result.scalars().all()

    async def _get_first_by_attribute(
        self, attribute: str, value: str, session: AsyncSession
    ) -> list[ModelType]:
        attr = getattr(self.model, attribute)
        db_obj = await session.execute(select(self.model).where(attr == value))
        return db_obj.scalars().first()

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        db_obj = await session.execute(select(self.model))
        return db_obj.scalars().all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        return await self._commit_and_refresh(db_obj, session)

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self._commit_and_refresh(db_obj, session)

    async def delete(
        self, db_obj: ModelType, session: AsyncSession
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
