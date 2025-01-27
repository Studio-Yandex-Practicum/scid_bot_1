from aiogram.fsm.state import State, StatesGroup

class ManagerState(StatesGroup):
    authorized = State()
    new_orders = State()
    order_in_progress = State()


class ContactRequestState(StatesGroup):
    start = State()
    enter_question= State()
    enter_contact_via = State()
    enter_phone = State()
    enter_email = State()
    end = State()