from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class MenuButton(Base):
    label: Mapped[str] = mapped_column(String, nullable=False)
    content_text: Mapped[str] = mapped_column(String, nullable=True)
    content_image: Mapped[str] = mapped_column(String, nullable=True)
    content_link: Mapped[str] = mapped_column(String, nullable=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey('menubutton.id'), 
        nullable=True
    )
    is_main_menu_button: Mapped[bool] = mapped_column(Boolean, default=False)

    children: Mapped[list['MenuButton']] = relationship(
        'MenuButton',
        backref='parent',
        remote_side=[id]
    )

    def __repr__(self):
        return (
            f"<MenuButton(text={self.label}, parent_id={self.parent_id})>"
        )
