from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, default="New User"
    )
    is_manager: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    telegram_user_id: Mapped[str] = mapped_column(String, nullable=True)
    manager_contact_requests: Mapped['ContactRequest'] = relationship(
        'ContactRequest', back_populates='manager', lazy='joined'
    )