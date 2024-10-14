from aiogram.fsm.state import State, StatesGroup

class ManagerState(StatesGroup):
    authorized = State()
    new_orders = State()