from fastapi import Depends, HTTPException, status

from core.users import current_user
from models.user import User


async def get_manager_or_superuser(
    current_user: User = Depends(current_user),
) -> User:
    if not current_user.is_manager and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Доступно только для менеджера или администратора.',
        )
    return current_user
