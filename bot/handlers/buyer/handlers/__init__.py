from aiogram.dispatcher.router import Router
from .base import router as _base_router
from .buy_product import buyer_router as _buyer_handler_router

buyer_router = Router()
buyer_router.include_routers(_base_router, _buyer_handler_router)
__all__ = ['buyer_router']