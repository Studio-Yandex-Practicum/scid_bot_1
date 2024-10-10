from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import main_router
from core.config import settings
from core.db import async_session_maker
from services.bot_menu import create_main_menu_button
from services.fixtures import load_fixtures
from services.users import create_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_user(
        email=settings.db.first_superuser_email,
        name="Администратор",
        telegram_user_id=None,
        password=settings.db.first_superuser_password,
        is_superuser=True,
        is_manager=True,
    )
    async with async_session_maker() as session:
        await create_main_menu_button(session)
        if settings.app.load_demo_data_fixtures:
            await load_fixtures("fixtures/presentation.yaml", session)
    yield


app = FastAPI(
    title=settings.app.app_title,
    description=settings.app.app_description,
    lifespan=lifespan,
)
app.include_router(main_router)
