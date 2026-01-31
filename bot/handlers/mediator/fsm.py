from aiogram.fsm.state import State, StatesGroup

class MediatorStates(StatesGroup):
    enter_new_msg = State()
    enter_new_answer = State()

    check_chat = State()
