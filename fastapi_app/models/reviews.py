from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from core.db import Base


class Review(Base):
    telegram_user_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return (
            f"<Review(id={self.id}, telegram_user_id="
            f"{self.telegram_user_id}, rating={self.rating}, "
            f"created_at={self.created_at}"
        )
