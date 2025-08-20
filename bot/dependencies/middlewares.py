from aiogram import BaseMiddleware

from bot.services.product.services import ProductService


class DIProductServiceMiddleware(BaseMiddleware):
    def __init__(self, product_service: ProductService):
        self._product_service = product_service

    async def __call__(self, handler, event, data: dict):
        data['product_service'] = self._product_service
        return await handler(event, data)
