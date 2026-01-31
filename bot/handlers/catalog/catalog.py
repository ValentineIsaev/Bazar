from typing import Callable, Awaitable, ParamSpecKwargs, Any

from aiogram import Bot
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from bot.types.storage import FSMStorage
from bot.types.utils import CallbackSetting, MessageSetting

from bot.utils.message_utils import  send_message, send_text_message
from bot.utils.filters import CallbackFilter

from bot.managers.catalog_manager import CatalogManager, ScrollModes
from bot.components.product_renderer import skip_buyer_product_renderer

from bot.handlers.buyer.fsm import BuyerStates

catalog_menu_router = Router()


SCROLL_MODES = {
    'next': ScrollModes.SCROLL_NEXT,
    'back': ScrollModes.SCROLL_BACK
}
async def _catalog_control(cb: CallbackQuery, fsm_storage: FSMStorage, catalog_manager: CatalogManager,
                           send_method: Callable[[Bot, FSMStorage, MessageSetting, dict[str, Any]], Awaitable[None]],
                           method_kwargs):
    _, subscope, action = CallbackSetting.decode_callback(cb.data)

    if subscope == 'scroll':
        await catalog_manager.scroll_catalog(SCROLL_MODES.get(action))
        await send_method(cb.bot, fsm_storage, await catalog_manager.render_message(), method_kwargs)


async def _send_next_product(bot: Bot, fsm_storage: FSMStorage, new_msg, data):
    catalog_manager: CatalogManager = data.get('catalog_manager')
    media_consolidator = data.get('media_consolidator')
    await catalog_manager.scroll_catalog(ScrollModes.SCROLL_BACK)
    product = await catalog_manager.get_page()

    await send_text_message(fsm_storage, bot,
                            skip_buyer_product_renderer.render_product(product[0][1], media_consolidator), False)

    await catalog_manager.scroll_catalog(ScrollModes.SCROLL_NEXT)
    await send_message(fsm_storage, bot, new_msg)


@catalog_menu_router.callback_query(CallbackFilter('catalog_menu'), StateFilter(BuyerStates.scroll_products))
async def scroll_product_catalog_menu(cb: CallbackQuery, fsm_storage: FSMStorage, catalog_manager: CatalogManager,
                                      media_consolidator):
    method_kwargs = {'catalog_manager': catalog_manager,
                     'media_consolidator': media_consolidator}
    await _catalog_control(cb, fsm_storage, catalog_manager, _send_next_product,
                           method_kwargs
    )


@catalog_menu_router.callback_query(CallbackFilter('catalog_menu'))
async def scroll_catalog_menu(cb: CallbackQuery, fsm_storage: FSMStorage, catalog_manager: CatalogManager):
    await _catalog_control(cb, fsm_storage, catalog_manager, lambda bot_, fsm_storage_, msg_, _: send_message(fsm_storage_,
                                                                                                           bot_,
                                                                                                           msg_,
                                                                                                              False),
                           {})