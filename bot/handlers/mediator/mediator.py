from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram.types import Message
from .messages import *

from bot.types.storage import FSMStorage
from bot.types.storage import TelegramMediaLocalConsolidator, TelegramMediaSaveData
from bot.utils.filters import CallbackFilter
from aiogram.filters import StateFilter
from bot.types.utils import CallbackSetting
from bot.types.managers import MediatorManager, CatalogManager
from bot.types.utils import MessageSetting
from bot.utils.message_utils import send_message
from bot.constants.utils_const import TypesMedia

from bot.configs.constants import UserTypes

from bot.constants.redis_keys import UserSessionKeys, FSMKeys
from bot.services.product import Product
from bot.services.catalog_service import CatalogMenuService
from bot.services.mediator_chat import Chat, ChatMessage

from bot.components.catalog_renderer import MediatorChatsRenderer

from .states import MediatorStates

mediator_router = Router()


@mediator_router.callback_query(CallbackFilter('mediator_chat', 'chat'))
async def chat_processing(cb: CallbackQuery, mediator_manager: MediatorManager[MessageSetting],
                          fsm_storage: FSMStorage, catalog_manager: CatalogManager):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)

    user_id = cb.from_user.id
    # user_role = await fsm_storage.get_value(FSMKeys.USERTYPE)
    user_role = UserTypes.BUYER
    new_msg: MessageSetting | None = None
    if action == 'start':
        product: Product = await fsm_storage.get_value(UserSessionKeys.TEMP_PRODUCT)
        chat = await mediator_manager.start_chat(product.autor_id,
                                                 user_id,
                                                 product.product_id,
                                                 product.name_product)
        await fsm_storage.update_value(UserSessionKeys.MEDIATOR_CHAT, chat)
        new_msg = await mediator_manager.get_render_msgs(chat.chat_id, user_id)
    elif action == 'get_chats':
        chats = await mediator_manager.get_chats(user_id, user_role)
        catalog_service = CatalogMenuService(tuple((i, chat) for i, chat in enumerate(chats)), 5)
        catalog_renderer = MediatorChatsRenderer(CallbackSetting(scope, 'msgs', 'get'))

        await catalog_manager.set_catalog_service(catalog_service)
        await catalog_manager.set_renderer(catalog_renderer)

        new_msg = await catalog_manager.render_message()
    elif action == 'delete':
        pass

    if new_msg is not None:
        await send_message(fsm_storage, cb.bot, new_msg)

@mediator_router.callback_query(CallbackFilter('mediator_chat', 'msgs'))
async def msgs_processing(cb: CallbackQuery, mediator_manager: MediatorManager[MessageSetting],
                          fsm_storage: FSMStorage, catalog_manager: CatalogManager, state: FSMContext):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    user_id = cb.from_user.id

    new_msg: MessageSetting | None = None
    if action == 'send':
        await state.set_state(MediatorStates.enter_new_msg)
        new_msg = INPUT_MEDIATOR_MSG
    elif action.startswith('get'):
        selected_chat: Chat = await catalog_manager.get_catalog_by_callback(cb.data)
        await fsm_storage.update_value(UserSessionKeys.MEDIATOR_CHAT, selected_chat)
        new_msg = await mediator_manager.get_render_msgs(selected_chat.chat_id, user_id)

    if new_msg is not None:
        await send_message(fsm_storage, cb.bot, new_msg)


@mediator_router.message(StateFilter(MediatorStates.enter_new_msg))
async def send_msg(msg: Message, media_consolidator: TelegramMediaLocalConsolidator,
                   mediator_manager: MediatorManager[MessageSetting], fsm_storage: FSMStorage,
                   state: FSMContext):
    mediator_chat: Chat = await fsm_storage.get_value(UserSessionKeys.MEDIATOR_CHAT)

    path = None
    if msg.photo is not None:
        path = await media_consolidator.save_perm_obj((TelegramMediaSaveData(msg.photo[-1].file_id,
                                                                             TypesMedia.TYPE_PHOTO),))[0]
    elif msg.video is not None:
        path = await media_consolidator.save_perm_obj((TelegramMediaSaveData(msg.video.file_id,
                                                                             TypesMedia.TYPE_VIDEO),))[0]
    text = msg.text

    result = await mediator_manager.send_msg(ChatMessage(mediator_chat.chat_id, sender_id=msg.from_user.id,
                                                         text=text, media=path))
    if not result:
        reply_msg = await mediator_manager.get_render_msgs(mediator_chat.chat_id, msg.from_user.id)
        await state.set_state(MediatorStates.check_chat)
    else:
        reply_msg = ERROR_ENTERS_REPLY_MSGS.get(result)
    await send_message(fsm_storage, msg.bot, reply_msg)
