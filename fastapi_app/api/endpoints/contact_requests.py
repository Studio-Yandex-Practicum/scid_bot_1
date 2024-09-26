from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_async_session
from schemas import ContactRequestCreate, ContactRequestUpdate, ContactRequestResponse
from models import ContactRequest
from crud import contact_request_crud

router = APIRouter(prefix='/contact_requests', tags=['ContactRequests'])


@router.post('/', response_model=ContactRequestResponse)
async def create_contact_request(
    contact_request: ContactRequestCreate,
    session: AsyncSession = Depends(get_async_session),
    user_id: int = 1234,
):
    contact_request_db = await contact_request_crud.create(
        obj_in=contact_request,
        user_id=user_id,
        session=session
    )
    return contact_request_db


@router.get('/{request_id}', response_model=ContactRequestResponse)
async def get_contact_request(
    request_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    contact_request_db = await contact_request_crud.get(request_id, session)
    if not contact_request_db:
        raise HTTPException(status_code=404, detail="Request not found")
    return contact_request_db


@router.patch('/{request_id}', response_model=ContactRequestResponse)
async def update_contact_request(
    request_id: int,
    contact_request: ContactRequestUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    contact_request_db = await contact_request_crud.update(request_id, contact_request, session)
    return contact_request_db


@router.delete('/{request_id}', response_model=ContactRequestResponse)
async def delete_contact_request(
    request_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await contact_request_crud.delete(request_id, session)
