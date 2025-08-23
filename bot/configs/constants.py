from enum import Enum

class UserTypes:
    BUYER = 'buyer' # Покупатель товара
    SELLER = 'seller' # Продавец товара
    OPERATOR = 'operator' # Модератор товара
    ADMIN = 'admin' # Модератор бота
    ANALYST = 'analyst' # Аналитик работы бота
    DEFAULTS = 'defaults' # Пользователь, невыбравший роль


class UserSessionKeys(Enum):
    USERNAME = 'user_name'
    USERTYPE = 'user_type'
    CHAT_ID = 'chat_id'

    BOTS_MESSAGE = 'bots_message'
    BOTS_MEDIA_MESSAGE = 'bots_media_message'


class FSMKeys(Enum):
    CATALOG_MANAGER = 'catalog_manager'

    class InputMediaAlbum(Enum):
        INPUTS_MEDIA_MESSAGES = 'input_media_messages'
        SENT_BOTS_MESSAGES = 'sent_bots_messages'

    class SellerKeys(Enum):
        ADD_PRODUCT_MANAGER = 'add_product_manager'


# class ParamFSM:
#     class UserData:
#         NAME = 'name'
#         TYPE_USER = 'type_user'
#         RATING = 'rating'
#         MONEY = 'money'
#     class BotMessagesData:
#         CHAT_ID = 'chat_id'
#         BOT_MESSAGE = 'bot_message'
#         BOT_MEDIA_MESSAGE = 'media_message'
#         CATALOG_MANAGER = 'catalog_manager'
#         class InputMediaAlbum:
#             INPUTS_MEDIA = 'input_media'
#             BOTS_MESSAGES = 'answer_media_bots_messages'
#     class SellerData:
#         ADD_PRODUCT_OPERATOR = 'add_product_operator'
#
#
# PASS_CALLBACK = '_'
ROW_BUTTON_CATALOG_MENU = 4
