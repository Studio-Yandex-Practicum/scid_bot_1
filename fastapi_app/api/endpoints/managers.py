from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.users_validators import (
    check_email_not_use,
    check_user_is_manager,
    check_user_is_not_superuser,
)
from core.db import get_async_session
from core.users import current_superuser
from crud.user import user_crud
from models.user import User
from schemas.users import (
    ManagerCreate,
    ManagerUpdate,
    UserContactRequestResponse
)
from services.users import create_user

router = APIRouter(prefix='/managers', tags=['managers'])


@router.post(
    '/',
    response_model=UserContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary='Добавляет Менеджера',
)
async def create_manager(
    new_user: ManagerCreate, session: AsyncSession = Depends(get_async_session)
) -> User:
    await check_email_not_use(user_email=new_user.email, session=session)
    return await create_user(
        email=new_user.email,
        name=new_user.name,
        password=new_user.password,
        telegram_user_id=new_user.telegram_user_id,
        is_manager=True,
        is_superuser=False,
    )


@router.get(
    '/all',
    response_model=list[UserContactRequestResponse],
    dependencies=[Depends(current_superuser)],
    summary='Получает всех менеджеров',
)
async def get_all_managers(
    session: AsyncSession = Depends(get_async_session),
) -> list[User]:
    return await user_crud.get_all_managers(session=session)


@router.get(
    '/{manager_id}',
    response_model=list[UserContactRequestResponse],
    dependencies=[Depends(current_superuser)],
    summary='Получает менеджера',
)
async def get_manager(
    manager_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    return await user_crud.get(
        obj_id=manager_id,
        session=session
    )


@router.patch(
    "/{manager_id}",
    response_model=UserContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary="Обновляет менеджера",
    description=("Возможно обновить только имя и telegram-id."),
)
async def update_manager(
    manager_id: int,
    manager: ManagerUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await user_crud.update(
        db_obj=await check_user_is_manager(
            user_id=manager_id,
            session=session,
        ),
        obj_in=manager,
        session=session,
    )


@router.delete(
    '/{user_id}',
    response_model=UserContactRequestResponse,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет менеджера',
)
async def delete_manager(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user = await check_user_is_manager(
        user_id=user_id,
        session=session,
    )
    await check_user_is_not_superuser(user)
    return await user_crud.delete(
        db_obj=user,
        session=session,
    )
