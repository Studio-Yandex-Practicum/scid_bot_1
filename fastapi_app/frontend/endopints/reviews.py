from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import check_user_is_superuser
from api.reviews_validators import check_review_exist
from api.endpoints.reviews import get_average_rating, delete_review
from core.db import get_async_session
from core.frontend import templates
from crud.reviews import reviews_crud

from models.user import User
from services.frontend import redirect_by_httpexeption

router = APIRouter(
    tags=['frontend_reviews'],
    prefix='/fr_reviews'
)


@router.get(
    '/list',
    response_class=HTMLResponse,
    summary='Список отзывов'
)
async def reviews_main(
    request: Request,
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    reviews = await reviews_crud.get_all(session=session)
    reviews.sort(
        key=lambda review: review.created_at, reverse=True
    )
    avg_rating = await get_average_rating(
        start_date=None,
        end_date=None,
        session=session
    )
    context = {
        'request': request,
        'user': user,
        'reviews': reviews,
        'avg_rating': round(avg_rating['average_rating'], 1)
    }
    return templates.TemplateResponse(
        'reviews/reviews_list.html', context
    )


@router.get(
    '/{review_id}',
    response_class=HTMLResponse,
    summary='Страница информации об отзыве',
)
async def review_details(
    request: Request,
    review_id: int,
    user: User = Depends(check_user_is_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        review = await check_review_exist(
            review_id=review_id, session=session
        )
    except HTTPException:
        await redirect_by_httpexeption(
            location=f'/?navbar_error={quote(
                'Отзыва не существует'
            )}'
        )
    context = {
        'request': request,
        'user': user,
        'review': review,
    }
    return templates.TemplateResponse(
        'reviews/review_details.html', context
    )


@router.delete(
    '/{review_id}',
    response_class=HTMLResponse,
    summary='Удалить отзыв',
    dependencies=[Depends(check_user_is_superuser)]
)
async def review_delete(
    request: Request,
    review_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await delete_review(
        review_id=review_id,
        session=session
    )
    return JSONResponse(
        content={ 'url': str(request.url_for('reviews_main')) }
    )