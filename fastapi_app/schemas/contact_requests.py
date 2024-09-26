from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContactRequestBase(BaseModel):
    telegram_user_id: str
    name: str
    phone: str
    contact_via_telegram: Optional[bool] = Field(default=False)
    contact_via_phone: Optional[bool] = Field(default=False)


class ContactRequestCreate(ContactRequestBase):
    pass


class ContactRequestUpdate(BaseModel):
    is_processed: Optional[bool] = Field(None)
    contact_via_telegram: Optional[bool] = Field(None)
    contact_via_phone: Optional[bool] = Field(None)


class ContactRequestResponse(ContactRequestBase):
    id: int
    is_processed: bool
    created_at: datetime = Field(...)
    closed_at: Optional[datetime] = Field(None)

    class Config:
        from_attributes = True
