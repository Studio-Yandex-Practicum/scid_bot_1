from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class ContactRequest(Base):
    telegram_user_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    contact_via_telegram: Mapped[bool] = mapped_column(Boolean, default=False)
    contact_via_phone: Mapped[bool] = mapped_column(Boolean, default=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self):
        return (
            f'<ContactRequest(id={self.id}, telegram_user_id='
            f'{self.telegram_user_id}, is_processed={self.is_processed}, '
            f'created_at={self.created_at}, created_at={self.created_at})>'
        )
