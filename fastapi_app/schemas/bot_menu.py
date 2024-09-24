from typing import Optional

from pydantic import BaseModel, field_validator


class MenuButtonBase(BaseModel):
    label: str
    content_text: Optional[str] = None
    content_image: Optional[str] = None
    content_link: Optional[str] = None


class MenuButtonCreate(MenuButtonBase):
    pass


class MenuButtonCreateMainButton(MenuButtonCreate):
    parent_id: Optional[int] = None
    is_main_menu_button: bool = True


class MenuButtonUpdate(MenuButtonBase):
    label: Optional[str]


class MenuButtonResponse(MenuButtonBase):
    id: int
    parent_id: Optional[int]

    class Config:
        from_attributes = True


class MenuButtonChildrenResponse(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]

    class Config:
        from_attributes = True


class MenuButtonFileBase(BaseModel):
    file_path: str
    file_type: str


class MenuButtonFileCreate(MenuButtonFileBase):
    button_id: int


class MenuButtonFileUpdate(MenuButtonFileBase):
    pass


class MenuButtonFileResponse(MenuButtonFileBase):
    id: int
    button_id: int

    class Config:
        from_attributes = True
