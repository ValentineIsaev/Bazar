class UserSessionKeys:
    USERNAME = 'user_name'
    CHAT_ID = 'chat_id'

    BOTS_MESSAGE_ID = 'bots_message'
    BOTS_MEDIA_MESSAGE_ID = 'bots_media_message'

    INPUT_PRODUCT_SERVICE = 'input_product_service'

    PRODUCT_MESSAGE_ID = 'product_message_id'
    PRODUCT_MEDIA_MESSAGE_ID = 'product_media_message_id'

    TEMP_PRODUCT = 'temp_product'


class FSMKeys:
    USER_ASYNC_LOCK = 'async_lock'

    TEMP_BOT_MSG = 'temp_bot_message'
    USERS_MEDIA_MSGS = 'user_media_msgs'
    SAVED_MEDIA_DATA = 'saved_media_data'

    class EditProduct:
        USER_PRODUCT_LIST = 'user_product_list'

    class CatalogData:
        CATALOG_RENDERER = 'catalog_renderer'
        CATALOG_SERVICE = 'catalog_service'
    USERTYPE = 'user_type'

    class InputMediaAlbum:
        INPUTS_MEDIA_MESSAGES_ID = 'input_media_messages'
        SENT_BOTS_MESSAGES_ID = 'sent_bots_messages'
    #
    # class SellerKeys:
    #     INPUT_PRODUCT_SERVICE = 'input_product_service'
