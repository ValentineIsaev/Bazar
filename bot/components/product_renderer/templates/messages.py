from bot.types.utils import TextTemplate
from bot.utils.message_utils.config_obj import MessageSetting

PRODUCT_TEXT = TextTemplate('🗂 Каталог: ?\n🧸 Название: ?\n\n📄 Описание: ?\n\n💰 Стоимость: ?')

ADD_PRODUCT_TEXT = '📦 *Данные о вашем товаре\\:\n\n*'
DELETE_PRODUCT_TEXT  = '\n\nВы действительно хотите удалить товар?'

MEDIATOR_TEXT = '\n\nПожалуйста, введите ваш вопрос. В вопросе можно использовать текст и одно медиа.'