from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers import main_router
from core.config import settings
from core.db import async_session_maker
from frontend.routers import frontend_router
from services.bot_menu import create_main_menu_button
from services.fixtures import load_fixtures
from services.users import create_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_user(
        email=settings.db.first_superuser_email,
        name='Администратор',
        telegram_user_id=settings.db.first_superuser_tg_id,
        password=settings.db.first_superuser_password,
        is_superuser=True,
        is_manager=True,
    )
    await create_user(
        email='test@test.com',
        name='Тест Менеджер',
        telegram_user_id='test',
        password='test',
        is_superuser=False,
        is_manager=True,
    )
    await create_user(
        email='test2@test2.com',
        name='Тест Подозрительный',
        telegram_user_id='test2',
        password='test',
        is_superuser=False,
        is_manager=False,
    )
    async with async_session_maker() as session:
        await create_main_menu_button(session)
        if settings.app.load_demo_data_fixtures:
            await load_fixtures(
                'fixtures/presentation.yaml',
                'fixtures/images',
                session
            )
    yield


app = FastAPI(
    title=settings.app.app_title,
    description=settings.app.app_description,
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/files", StaticFiles(directory="files"), name="files")
app.include_router(main_router)
app.include_router(frontend_router)
