from crud.base import CRUDBase
from models.bot_menu import MenuButton
from schemas.bot_menu import MenuButtonCreate, MenuButtonUpdate

class CRUDBotMenu(
    CRUDBase[MenuButton, MenuButtonCreate, MenuButtonUpdate]
):
    def __init__(self) -> None:
        super().__init__(MenuButton)


bot_menu_crud = CRUDBotMenu()