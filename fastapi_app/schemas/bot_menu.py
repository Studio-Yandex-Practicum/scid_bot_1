from typing import Optional

from pydantic import BaseModel, HttpUrl


class MenuButtonBase(BaseModel):
    label: str
    content_text: Optional[str] = None
    content_image: Optional[str] = None
    content_link: Optional[HttpUrl] = None
    parent_id: Optional[int] = None
    is_main_menu_button: bool = False


class MenuButtonCreate(MenuButtonBase):
    pass


class MenuButtonUpdate(MenuButtonBase):
    pass


class MenuButtonResponse(MenuButtonBase):
    id: int

    class Config:
        orm_mode = True


class MenuButtonChildrenResponse:
    id: int
    children: list['MenuButtonResponse'] = []

    class Config:
        orm_mode = True
