from aiogram.fsm.state import State, StatesGroup


class SellerStates(StatesGroup):
    seller_menu = State()