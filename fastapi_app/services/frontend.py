from fastapi import HTTPException, status


async def redirect_by_httpexeption(location: str):
    raise HTTPException(
        headers={"location": location},
        status_code=status.HTTP_302_FOUND,
    )
