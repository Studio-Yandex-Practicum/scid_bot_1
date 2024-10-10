from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.reviews import reviews_crud
from models.reviews import Review


async def check_review_exist(
    review_id: int,
    session: AsyncSession,
) -> Optional[Review]:
    return await check_object_exist(
        review_id,
        reviews_crud,
        f"Отзыв с id {review_id} не существует.",
        session,
    )
