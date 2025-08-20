from aiogram.fsm.context import FSMContext

from bot.services.product.services import ProductService

async def get_product_service():
    return ProductService()
