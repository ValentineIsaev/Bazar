from abc import abstractmethod

from .base import ProductRenderer
from .templates import (PRODUCT_TEXT, ADD_PRODUCT_TEXT, MEDIATOR_TEXT, BUY_PRODUCT_KEYBOARD,
                        DELETE_PRODUCT_TEXT)

from bot.types.utils import MessageSetting, MediaSetting, CallbackSetting, InlineButtonSetting, ParseModes
from bot.types.storage import TelegramMediaLocalConsolidator

from bot.utils.message_utils import get_callback_inline_keyboard

from bot.services.product import Product


class TelegramProductRenderer(ProductRenderer[MessageSetting]):
    @abstractmethod
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        pass

    def _render_product_data(self, product: Product,
                             media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        return MessageSetting(text=PRODUCT_TEXT.insert((product.catalog, product.name_product, product.description,
                                                        product.price)),
                              media=tuple(MediaSetting(type_media=media.type_media, path=media.path)
                        for media in media_consolidator.get_obj_data(*product.media_path)) \
                if product.media_path is not None else None,
                              parse_mode=ParseModes.MARKDOWN_V2)


class SellerProductRenderer(TelegramProductRenderer):
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        product_msg = self._render_product_data(product, media_consolidator)
        product_msg.text = ADD_PRODUCT_TEXT + product_msg.text

        return product_msg


class MediatorProductRenderer(TelegramProductRenderer):
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        product_msg = self._render_product_data(product, media_consolidator)
        product_msg.text += MEDIATOR_TEXT

        return product_msg


class BuyerProductRenderer(TelegramProductRenderer):
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        product_msg = self._render_product_data(product, media_consolidator)
        product_msg.keyboard = BUY_PRODUCT_KEYBOARD

        return product_msg


class BuyerSkipProductRenderer(TelegramProductRenderer):
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        return self._render_product_data(product, media_consolidator)


class DeleteProductRenderer(TelegramProductRenderer):
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        product_msg = self._render_product_data(product, media_consolidator)
        product_msg.text += DELETE_PRODUCT_TEXT
        # product_msg.keyboard = DELETE_PRODUCT_KEYBOARD

        return product_msg


class OnlyProductRenderer(TelegramProductRenderer):
    def render_product(self, product: Product,
                       media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
        return self._render_product_data(product, media_consolidator)