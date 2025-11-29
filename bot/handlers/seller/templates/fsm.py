from bot.services.product import ProductInputField
from dataclasses import dataclass
from aiogram.fsm.state import State, StatesGroup

from bot.utils.message_utils.config_obj import MessageSetting

from .messages import *


class SellerStates(StatesGroup):
    seller_menu = State()


class EditProductStates(StatesGroup):
    delete_product = State()
    edit_product = State()

    set_name_edit_product = State()
    set_name_delete_product = State()

    choose_param = State()
    class EditParam(StatesGroup):
        edit_name = State()
        edit_price = State()
        edit_photo = State()
        edit_catalog = State()
        edit_description = State()
    complete_edit = State()


class AddProductStates(StatesGroup):
    choose_catalog = State()
    add_name = State()
    add_description = State()
    add_photo = State()
    add_price = State()
    user_checking = State()
    complete = State()


@dataclass
class StateData:
    field_name: ProductInputField
    next_state: State=None
    new_msg: MessageSetting=None


PRODUCT_STATES_DATA = {
    AddProductStates.choose_catalog: StateData(ProductInputField.CATALOG.value, AddProductStates.add_name,
                                               INPUT_PRODUCT_NAME_MESSAGE),
    AddProductStates.add_name: StateData(ProductInputField.NAME_PRODUCT.value, AddProductStates.add_description,
                                         INPUT_DESCRIPTION_MESSAGE),
    AddProductStates.add_description: StateData(ProductInputField.DESCRIPTION.value, AddProductStates.add_photo,
                                                INPUT_PHOTO_PRODUCT_MESSAGE),
    AddProductStates.add_photo : StateData(ProductInputField.MEDIA_PATH.value, AddProductStates.add_price,
                                           INPUT_PRICE_PRODUCT_MESSAGE),
    AddProductStates.add_price: StateData(ProductInputField.PRICE.value, AddProductStates.user_checking),

    EditProductStates.EditParam.edit_catalog: StateData(ProductInputField.CATALOG.value, AddProductStates.user_checking),
    EditProductStates.EditParam.edit_price: StateData(ProductInputField.PRICE.value, AddProductStates.user_checking),
    EditProductStates.EditParam.edit_photo: StateData(ProductInputField.MEDIA_PATH.value,
                                                      AddProductStates.user_checking),
    EditProductStates.EditParam.edit_name: StateData(ProductInputField.NAME_PRODUCT.value,
                                                     AddProductStates.user_checking),
    EditProductStates.EditParam.edit_description: StateData(ProductInputField.DESCRIPTION.value,
                                                            AddProductStates.user_checking)
}

EDIT_PRODUCT_MESSAGES = {
    EditProductStates.EditParam.edit_name: INPUT_PRODUCT_NAME_MESSAGE,
    EditProductStates.EditParam.edit_price: INPUT_PRICE_PRODUCT_MESSAGE,
    EditProductStates.EditParam.edit_photo: INPUT_PHOTO_PRODUCT_MESSAGE,
    EditProductStates.EditParam.edit_description: INPUT_DESCRIPTION_MESSAGE
}
