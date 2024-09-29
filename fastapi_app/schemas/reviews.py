from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    telegram_user_id: str = Field(...)
    text: str = Field(...)
    rating: int = Field(..., ge=1, le=5)


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewPaginationResponse(BaseModel):
    count: int
    total: int
    reviews: list[ReviewResponse]
