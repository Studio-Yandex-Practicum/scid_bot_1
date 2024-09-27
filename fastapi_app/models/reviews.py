from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from core.db import Base


class Review(Base):
    telegram_user_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f'<Review(id={self.id}, telegram_user_id='
            f'{self.telegram_user_id}, rating={self.rating}, '
            f'created_at={self.created_at}'
        )
