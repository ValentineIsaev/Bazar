from aiogram.fsm.state import State, StatesGroup

class SellerStates(StatesGroup):
    seller_menu = State()


class EditProductStates(StatesGroup):
    group_name = 'EditProductStates'

    choose_param = State()
    class EditParam(StatesGroup):
        edit_name = State()
        edit_price = State()
        edit_photo = State()
        edit_catalog = State()
        edit_description = State()
    complete_edit = State()


EDIT_PARAM_PRODUCT_STATES = {
            'name': EditProductStates.EditParam.edit_name,
            'price': EditProductStates.EditParam.edit_price,
            'photo': EditProductStates.EditParam.edit_photo,
            'catalog': EditProductStates.EditParam.edit_catalog,
            'description': EditProductStates.EditParam.edit_description
}



class AddProductStates(StatesGroup):
    group_name = 'AddProductStates'

    choose_catalog = State()
    add_name = State()
    add_description = State()
    add_photo = State()
    add_price = State()
    user_checking = State()
    complete = State()