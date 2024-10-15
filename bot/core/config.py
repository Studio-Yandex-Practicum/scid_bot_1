import os

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    token: str = None
    root_dir: Path = os.path.dirname(os.path.abspath(__module__))
    base_dir_for_files: Path = Path("files/")


class APIConfig(BaseModel):
    base_url: str = 'http://localhost'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BOT_CONFIG__",
    )
    app: AppConfig = AppConfig()
    api: APIConfig = APIConfig()


settings = Settings()


def create_dirs():
    results_dir = Path(settings.app.base_dir_for_files)
    results_dir.mkdir(exist_ok=True)


create_dirs()
