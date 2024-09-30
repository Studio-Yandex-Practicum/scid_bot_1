from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class ScidUserMixin:
    name: Optional[str]
    is_manager: Optional[bool] = Field(False)
    telegram_user_id: Optional[str]


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate, ScidUserMixin):
    pass


class UserUpdate(schemas.BaseUserUpdate, ScidUserMixin):
    pass


class UserPasswordUpdate(schemas.CreateUpdateDictModel):
    password: str
