class UserTypes:
    BUYER = 'buyer' # Покупатель товара
    SELLER = 'seller' # Продавец товара
    OPERATOR = 'operator' # Модератор товара
    ADMIN = 'admin' # Модератор бота
    ANALYST = 'analyst' # Аналитик работы бота
    DEFAULTS = 'defaults' # Пользователь, невыбравший роль

class ParamFSM:
    class UserData:
        NAME = 'name'
        TYPE_USER = 'type_user'
        RATING = 'rating'
        MONEY = 'money'
    class BotMessagesData:
        CHAT_ID = 'chat_id'
        BOT_MESSAGE = 'bot_message'
        BOT_MEDIA_MESSAGE = 'media_message'
        class InputMediaAlbum:
            INPUTS_MEDIA = 'input_media'
            BOTS_MESSAGES = 'answer_media_bots_messages'
    class ProductData:
        CATALOG_MENU = 'catalog_menu'
        PRODUCT = 'product'
        CATALOG_MENU_CALLBACK = 'catalog_callback'
    class SellerData:
        ADD_PRODUCT_OPERATOR = 'add_product_operator'
    class BuyerData:
        CATALOG_PRODUCT = 'catalog_product'

PASS_CALLBACK = '_'
ROW_BUTTON_CATALOG_MENU = 4
