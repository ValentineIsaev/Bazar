from bot.types.utils import MessageSetting, TextTemplate

from bot.constants.user_constants import TypesUser

CHAT_HEAD = TextTemplate('💬 *Чат "?"*\n\n')
MSG_FORM = TextTemplate('*?*\n?\n_\\(' r'?' '\\)_\n\n') #Sender role, msg, senderDate

ROLE_NAMES = {
    TypesUser.BUYER: '👾 Продавец',
    TypesUser.SELLER: '👾 Покупатель',
    'SELF': '👑 Вы'
}