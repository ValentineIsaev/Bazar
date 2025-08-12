from bot.utils.message_utils.keyboard_utils import InlineButtonSetting, create_callback

CATALOG_MENU_NEXT = (InlineButtonSetting(text='Вперед', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'next')),)
CATALOG_MENU_BACK = (InlineButtonSetting(text='Назад', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'back')),)