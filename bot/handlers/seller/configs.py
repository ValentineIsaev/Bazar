from dataclasses import dataclass
from typing import Callable

from aiogram.fsm.state import State

from .messages import *
from .fsm_states import EditProductStates, AddProductStates, SellerStates
from bot.services.product.validation_input_product import validate_price, validate_media

BASE_STATE = SellerStates.seller_menu

@dataclass
class FieldConfig:
    input_msg: MessageSetting | None = None
    next_field: str | None = None
    next_state: State | None = None
    validate_func: None | Callable = None

    is_end_field: bool = False


ADD_FIELD_PRODUCT_CONFIGS = {
    'name': FieldConfig(INPUT_PRODUCT_NAME_MESSAGE, 'description', AddProductStates.add_description),
    'catalog': FieldConfig(next_field='name', next_state=AddProductStates.add_name),
    'price': FieldConfig(INPUT_PRICE_PRODUCT_MESSAGE, None,
                         EditProductStates.complete_edit, validate_price, is_end_field=True),
    'description': FieldConfig(INPUT_DESCRIPTION_MESSAGE, 'photo', AddProductStates.add_photo),
    'photo': FieldConfig(INPUT_PHOTO_PRODUCT_MESSAGE, 'price', AddProductStates.add_price, validate_media)
}
