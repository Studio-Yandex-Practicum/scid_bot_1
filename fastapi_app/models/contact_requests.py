from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class ContactRequest(Base):
    telegram_user_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(
        String, nullable=False, default="Не указано"
    )
    phone: Mapped[str] = mapped_column(
        String, nullable=False, default="Не указано"
    )
    email: Mapped[str] = mapped_column(
        String, nullable=False, default="Не указано"
    )
    contact_via_telegram: Mapped[bool] = mapped_column(Boolean, default=False)
    contact_via_phone: Mapped[bool] = mapped_column(Boolean, default=False)
    contact_via_email: Mapped[bool] = mapped_column(Boolean, default=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    in_progress: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    manager_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    manager: Mapped[Optional["User"]] = relationship(
        "User", backref="manager_contact_requests"
    )
    text: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return (
            f"<ContactRequest(id={self.id}, telegram_user_id="
            f"{self.telegram_user_id}, is_processed={self.is_processed}, "
            f"created_at={self.created_at}, created_at={self.created_at})>"
        )
