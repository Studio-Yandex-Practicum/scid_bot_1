from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.reviews import Review
from schemas.reviews import ReviewCreate


class CRUDReviews(
    CRUDBase[Review, ReviewCreate, None]
):
    def __init__(self) -> None:
        super().__init__(Review)

    async def get_reviews_by_paginatoion(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 10, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> list[Review]:
        query = select(Review)
        if start_date and end_date:
            query = query.where(
                Review.created_at >= start_date, Review.created_at <= end_date
            )
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_reviews_count(
        self,
        session: AsyncSession, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        query = select(Review)
        if start_date and end_date:
            query = query.where(
                Review.created_at >= start_date, Review.created_at <= end_date
            )
        result = await session.execute(query)
        return result.scalars().count()

reviews_crud = CRUDReviews()
