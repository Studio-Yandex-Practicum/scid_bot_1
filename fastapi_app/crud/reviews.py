from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.reviews import Review
from schemas.reviews import ReviewCreate


class CRUDReviews(CRUDBase[Review, ReviewCreate, None]):
    def __init__(self) -> None:
        super().__init__(Review)

    async def _apply_date_range(
        self,
        query,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        session: AsyncSession,
    ):
        if start_date:
            query = query.where(Review.created_at >= start_date)
        if end_date:
            query = query.where(Review.created_at <= end_date)
        return await session.execute(query)

    async def get_reviews_by_paginatoion(
        self,
        offset: int,
        limit: int,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        session: AsyncSession,
    ) -> list[Review]:
        result = await self._apply_date_range(
            select(Review).offset(offset).limit(limit),
            start_date,
            end_date,
            session,
        )
        return result.scalars().all()

    async def get_reviews_count(
        self,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        session: AsyncSession,
    ) -> int:
        result = await self._apply_date_range(
            select(func.count()).select_from(Review),
            start_date,
            end_date,
            session,
        )
        return result.scalars().first()

    async def get_average_rating(
        self,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        session: AsyncSession,
    ):
        result = await self._apply_date_range(
            select(func.avg(Review.rating)), start_date, end_date, session
        )
        return result.scalar()


reviews_crud = CRUDReviews()
