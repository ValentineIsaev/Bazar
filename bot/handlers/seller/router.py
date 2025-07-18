from aiogram.dispatcher.router import Router

from .base.base import router as base_router
from .product import input_router, edit_router

seller_router = Router()
seller_router.include_routers(base_router, edit_router, input_router)
