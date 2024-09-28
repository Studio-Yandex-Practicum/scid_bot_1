from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    telegram_user_id: int = Field(..., example=12345678)
    text: str = Field(..., example='Great service!')
    rating: float = Field(..., ge=1, le=5, example=4.5)


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewPaginationResponse(BaseModel):
    total: int
    reviews: list[ReviewResponse]


class ReviewFilter(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
