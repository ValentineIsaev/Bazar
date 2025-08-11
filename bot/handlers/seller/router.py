from aiogram.dispatcher.router import Router

from .handlers.base import router as base_router
from .handlers.edit_fields_product_handler import router as edit_router
from .handlers.input_fields_product_handler import router as input_router

seller_router = Router()
seller_router.include_routers(base_router, edit_router, input_router)
