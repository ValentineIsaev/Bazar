from aiogram.fsm.state import State, StatesGroup


class BuyerStates(StatesGroup):
    main_menu = State()

    class HistoryProduct(StatesGroup):
        choice_product = State()
        set_rating = State()
        return_product = State()

    class BuyProduct(StatesGroup):
        choice_catalog = State()
        look_product = State()
        buy_product = State()
        set_rating = State()

