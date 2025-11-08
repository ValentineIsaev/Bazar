from dataclasses import dataclass

from aiogram.fsm.state import State

from bot.handlers.seller.templates.messages import *
from bot.handlers.seller.templates.fsm import EditProductStates, AddProductStates, SellerStates

BASE_STATE = SellerStates.seller_menu

@dataclass
class FieldConfig:
    input_msg: MessageSetting | None = None
    next_field: str | None = None
    next_state: State | None = None

    is_end_field: bool = False


# ADD_FIELD_PRODUCT_CONFIGS = {
#     'name_product': FieldConfig(INPUT_PRODUCT_NAME_MESSAGE, 'description', AddProductStates.add_description),
#     'catalog': FieldConfig(next_field='name_product', next_state=AddProductStates.add_name),
#     'price': FieldConfig(INPUT_PRICE_PRODUCT_MESSAGE, None,
#                          EditProductStates.complete_edit, is_end_field=True),
#     'description': FieldConfig(INPUT_DESCRIPTION_MESSAGE, 'media_path', AddProductStates.add_photo),
#     'media_path': FieldConfig(INPUT_PHOTO_PRODUCT_MESSAGE, 'price', AddProductStates.add_price)
# }
