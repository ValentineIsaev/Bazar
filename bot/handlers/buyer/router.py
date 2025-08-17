from aiogram.dispatcher.router import Router

from .handlers.base import router as base_router
from .handlers.buy_product import buyer_router

router = Router()
router.include_routers(base_router, buyer_router)
