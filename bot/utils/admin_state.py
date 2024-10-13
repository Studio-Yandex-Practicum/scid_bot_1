from aiogram.fsm.state import State, StatesGroup


class CreateButton(StatesGroup):
    typing_button_id = State()
    typing_button_name = State()
    typing_parent_id = State()
    typing_content_text = State()
    typing_content_link = State()
    adding_content_image = State()
    submiting_button = State()