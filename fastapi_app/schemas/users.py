from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field


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


class UserContactRequestResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    telegram_user_id: Optional[str]

    class Config:
        from_attributes = True


class ManagerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    telegram_user_id: str