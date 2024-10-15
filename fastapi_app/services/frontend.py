from typing import Any

from fastapi import HTTPException, status


async def redirect_by_httpexeption(location: str):
    raise HTTPException(
<<<<<<< HEAD
        headers={"location": location},
=======
        headers={'location': location},
>>>>>>> dev
        status_code=status.HTTP_302_FOUND,
    )
