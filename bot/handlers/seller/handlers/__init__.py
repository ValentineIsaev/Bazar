from aiogram.dispatcher.router import Router

from .base import router as _base_router
from .input_fields_product_handler import router as _enter_product_router
from .edit_fields_product_handler import router as _edit_product_router

seller_router = Router()
seller_router.include_routers(_base_router, _enter_product_router, _edit_product_router)
__all__ = ['seller_router']