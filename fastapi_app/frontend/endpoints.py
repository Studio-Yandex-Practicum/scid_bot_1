from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from core.users import current_user, current_superuser


router = APIRouter(tags=['frontend'])
templates = Jinja2Templates(directory="static/templates")


@router.get(
    '/',
    summary='Загрузка главной страницы',
    # dependencies=[Depends(current_user)]
)
async def create_review(
    request: Request
):
    context = {"request": request}
    return templates.TemplateResponse("base.html", context)
