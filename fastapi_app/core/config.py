from pathlib import Path
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    app_title: str = 'Настройка и взаимодействие с телеграм ботом scid'
    app_description: str = (
        'Позволяет настроить телеграм бот scid: создать меню, контент, '
        'добавить сотрудников поддержки, к которым может обратиться '
        'пользователь, а так же просмотреть отзывы клиентов'
    )
    base_dir_for_files: Path = Path(
        'files/'
    )   # При изменении папки сохранения
    # необхоидмо не забыть изменить настройки nginx и docker volume
    chunk_size: int = 1024


class DBConfig(BaseModel):
    database_url: str = None
    sheduler_database_url: str = None
    echo: bool = False
    echo_pool: bool = False
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


class SecurityConfig(BaseModel):
    secret: str = 'YOUR_SECRET_KEY'
    jwt_lifetime: int = 3500


class EmailConfig(BaseModel):
    mail_username: str = (None,)
    mail_password: str = (None,)
    mail_from: str = ('scid_bot_1@admin.com',)
    mail_port: int = (587,)
    mail_server: str = (None,)
    mail_from_name: str = ('scid_bot_1',)
    mail_starttls: bool = (True,)
    mail_ssl_tls: bool = (False,)
    use_credentials: bool = (True,)
    validate_certs: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    app: AppConfig = AppConfig()
    db: DBConfig = DBConfig()
    security: SecurityConfig = SecurityConfig()
    email: EmailConfig = EmailConfig()


settings = Settings()


def create_dirs():
    results_dir = Path(settings.app.base_dir_for_files)
    results_dir.mkdir(exist_ok=True)


create_dirs()
