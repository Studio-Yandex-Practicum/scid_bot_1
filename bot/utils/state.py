from aiogram.fsm.state import State, StatesGroup

class NavigationState(StatesGroup):
    at_menu = State()  # Состояние, где бот показывает текущее меню
