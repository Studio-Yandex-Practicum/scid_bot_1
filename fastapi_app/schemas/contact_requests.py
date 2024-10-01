from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from schemas.users import UserContactRequestResponse


class ContactRequestBase(BaseModel):
    telegram_user_id: str
    name: str
    phone: str
    email: str
    text: Optional[str] = Field(None)
    contact_via_telegram: Optional[bool] = Field(default=False)
    contact_via_phone: Optional[bool] = Field(default=False)
    contact_via_email: Optional[bool] = Field(default=False)


class ContactRequestCreate(ContactRequestBase):
    pass


class ContactRequestUpdate(BaseModel):
    is_processed: Optional[bool] = Field(None)
    in_progress: Optional[bool] = Field(None)
    contact_via_telegram: Optional[bool] = Field(None)
    contact_via_phone: Optional[bool] = Field(None)
    contact_via_email: Optional[bool] = Field(None)


class ContactRequestResponse(ContactRequestBase):
    id: int
    is_processed: bool
    in_progress: bool
    created_at: datetime = Field(...)
    closed_at: Optional[datetime] = Field(None)
    manager: Optional[UserContactRequestResponse] = Field(None)

    class Config:
        from_attributes = True
