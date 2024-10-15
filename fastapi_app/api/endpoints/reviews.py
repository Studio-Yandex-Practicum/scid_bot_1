from datetime import datetime
from typing import Optional

from api.reviews_validators import check_review_exist
from core.db import get_async_session
from core.users import current_superuser
from crud.reviews import reviews_crud
from fastapi import APIRouter, Depends, Query
from schemas.reviews import (ReviewCreate, ReviewPaginationResponse,
                             ReviewResponse)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse, summary="Добавляет отзыв")
async def create_review(
    review: ReviewCreate, session: AsyncSession = Depends(get_async_session)
):
    return await reviews_crud.create(obj_in=review, session=session)


@router.get(
    "/count",
    response_model=None,
    summary="Получает количество отзывов",
    description="Без диапазона дат вернёт количество всех отзывов",
)
async def get_reviews_count(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    total = await reviews_crud.get_reviews_count(
        session=session, start_date=start_date, end_date=end_date
    )
    return {"count": total}


@router.get(
    "/average_rating",
    response_model=None,
    summary="Получает средний рейтинг на основе отзывов",
    description="Без диапазона дат вернёт средний рейтинг за все отзывы",
)
async def get_average_rating(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "average_rating": await reviews_crud.get_average_rating(
            start_date=start_date, end_date=end_date, session=session
        )
    }


@router.get(
    "/",
    response_model=ReviewPaginationResponse,
    summary="Получает отзывы",
    description="Без диапазона дат вернёт все отзывы. Поддерживает пагинацию",
)
async def get_reviews(
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int] = Query(None, gt=0),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    reviews = await reviews_crud.get_reviews_by_paginatoion(
        offset=offset,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        session=session,
    )
    total = await reviews_crud.get_reviews_count(
        session=session, start_date=start_date, end_date=end_date
    )
    return ReviewPaginationResponse(
        count=len(reviews), total=total, reviews=reviews
    )


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Получает конкретный отзыв",
)
async def get_review(
    review_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await check_review_exist(review_id=review_id, session=session)


@router.delete(
    "/{review_id}",
    response_model=ReviewResponse,
    dependencies=[Depends(current_superuser)],
    summary="Удаляет отзыв",
)
async def delete_review(
    review_id: int,
    session: AsyncSession = Depends(get_async_session),
):

    return await reviews_crud.delete(
        db_obj=await check_review_exist(
            review_id=review_id,
            session=session,
        ),
        session=session,
    )
