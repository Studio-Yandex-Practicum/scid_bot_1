import enum

from core.db import Base
from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MenuButton(Base):
    label: Mapped[str] = mapped_column(String, nullable=False)
    content_text: Mapped[str] = mapped_column(String, nullable=True)
    content_image: Mapped[str] = mapped_column(String, nullable=True)
    content_link: Mapped[str] = mapped_column(String, nullable=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("menubutton.id"), nullable=True
    )
<<<<<<< HEAD
    parent: Mapped["MenuButton"] = relationship(
        "MenuButton",
        backref="button_parent",
        remote_side="MenuButton.id",
=======
    parent: Mapped['MenuButton'] = relationship(
        'MenuButton',
        backref='button_parent',
        remote_side='MenuButton.id',
>>>>>>> dev
        viewonly=True,
    )
    is_main_menu_button: Mapped[bool] = mapped_column(Boolean, default=False)

    children: Mapped[list["MenuButton"]] = relationship(
        "MenuButton", remote_side="MenuButton.id"
    )
    files: Mapped[list["MenuButtonFile"]] = relationship(
        back_populates="menu_button"
    )

    def __repr__(self):
        return f"<MenuButton(text={self.label}, parent_id={self.parent_id})>"


class MenuButtonFile(Base):
    button_id: Mapped[int] = mapped_column(
        ForeignKey("menubutton.id"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)

    menu_button: Mapped[MenuButton] = relationship(
        "MenuButton", back_populates="files"
    )

    def __repr__(self):
        return (
<<<<<<< HEAD
            f"<MenuButtonFile(button={self.button_id}, " f"{self.file_path})>"
=======
            f'<MenuButtonFile(button={self.button_id}, ' f'{self.file_path})>'
>>>>>>> dev
        )
