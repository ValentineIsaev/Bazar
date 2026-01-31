from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter

from .fsm import MediatorStates
from .messages import *

from bot.constants.user_constants import TypesUser
from bot.constants.utils_const import TypesMedia
from bot.constants.redis_keys import StorageKeys

from bot.types.storage import FSMStorage, TelegramMediaLocalConsolidator, TelegramMediaSaveData
from bot.types.managers import MediatorManager, CatalogManager
from bot.types.utils import CallbackSetting, MessageSetting

from bot.utils.filters import CallbackFilter
from bot.utils.message_utils import send_message, send_text_message

from bot.services.product import Product
from bot.services.catalog_service import CatalogMenuService
from bot.services.mediator_chat import Chat, ChatMessage

from bot.components.product_renderer import mediator_product_renderer, skip_buyer_product_renderer
from bot.components.catalog_renderer import MediatorChatsRenderer


mediator_router = Router()

async def start_chat(fsm_storage: FSMStorage, mediator_manager: MediatorManager[MessageSetting], user_id: int) -> Chat:
    product: Product = await fsm_storage.get_value(StorageKeys.TEMP_PRODUCT)
    chat = await mediator_manager.start_chat(product.autor_id,
                                             user_id,
                                             product.product_id,
                                             product.name_product)
    await fsm_storage.update_value(StorageKeys.MEDIATOR_CHAT, chat)

    return chat


@mediator_router.callback_query(CallbackFilter('mediator_chat', 'chat'))
async def chat_processing(cb: CallbackQuery, mediator_manager: MediatorManager[MessageSetting],
                          fsm_storage: FSMStorage, catalog_manager: CatalogManager):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)

    async def get_chats():
        chats = await mediator_manager.get_chats(user_id, user_role)
        catalog_service = CatalogMenuService(tuple((i, chat) for i, chat in enumerate(chats)), 5)
        catalog_renderer = MediatorChatsRenderer(CallbackSetting(scope, 'msgs', 'get_updates'),
                                                 CallbackSetting(scope, subscope, 'delete'))

        await catalog_manager.set_catalog_service(catalog_service)
        await catalog_manager.set_renderer(catalog_renderer)

    user_id = cb.from_user.id
    user_role: TypesUser = await fsm_storage.get_value(StorageKeys.USERTYPE)
    new_msg: MessageSetting | None = None
    if action == 'start':
        chat = await start_chat(fsm_storage, mediator_manager, user_id)
        new_msg = await mediator_manager.get_render_msgs(chat.chat_id, user_id)
    elif action == 'get_chats':
        await get_chats()
        new_msg = await catalog_manager.render_message()
    elif action.startswith('delete'):
        selected_chat: Chat = await catalog_manager.get_catalog_by_callback(CallbackSetting(*CallbackSetting.decode_callback(cb.data)))
        await mediator_manager.delete_chat(selected_chat.chat_id)

        await get_chats()
        new_msg = await catalog_manager.render_message()

    if new_msg is not None:
        await send_message(fsm_storage, cb.bot, new_msg, False)

@mediator_router.callback_query(CallbackFilter('mediator_chat', 'msgs'))
async def msgs_processing(cb: CallbackQuery, mediator_manager: MediatorManager[MessageSetting],
                          fsm_storage: FSMStorage, catalog_manager: CatalogManager, state: FSMContext,
                          media_consolidator: TelegramMediaLocalConsolidator):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    user_id = cb.from_user.id

    new_msg: MessageSetting | None = None
    if action == 'send':
        await state.set_state(MediatorStates.enter_new_msg)
        new_msg = INPUT_MEDIATOR_MSG

    elif action.startswith('get_updates'):
        selected_chat: Chat = await catalog_manager.get_catalog_by_callback(CallbackSetting(*CallbackSetting.decode_callback(cb.data)))
        await fsm_storage.update_value(StorageKeys.MEDIATOR_CHAT, selected_chat)
        new_msg = await mediator_manager.get_render_new_msgs(selected_chat.chat_id, user_id)
    elif action == 'get_all':
        selected_chat: Chat = await fsm_storage.get_value(StorageKeys.MEDIATOR_CHAT)
        new_msg = await mediator_manager.get_render_msgs(selected_chat.chat_id, user_id)

    if new_msg is not None:
        await send_message(fsm_storage, cb.bot, new_msg, False)


@mediator_router.callback_query(CallbackFilter('mediator_chat', 'send_answer'))
async def send_answer(cb: CallbackQuery, fsm_storage: FSMStorage, mediator_manager: MediatorManager,
                      media_consolidator: TelegramMediaLocalConsolidator, state: FSMContext):
    await state.set_state(MediatorStates.enter_new_msg)

    await start_chat(fsm_storage, mediator_manager, cb.from_user.id)

    product: Product = await fsm_storage.get_value(StorageKeys.TEMP_PRODUCT)
    product_msg = skip_buyer_product_renderer.render_product(product, media_consolidator)
    await send_text_message(fsm_storage, cb.bot, product_msg, False)

    await send_message(fsm_storage, cb.bot, INPUT_MEDIATOR_MSG)


@mediator_router.message(StateFilter(MediatorStates.enter_new_msg))
async def send_msg(msg: Message, media_consolidator: TelegramMediaLocalConsolidator,
                   mediator_manager: MediatorManager[MessageSetting], fsm_storage: FSMStorage,
                   state: FSMContext):
    mediator_chat: Chat = await fsm_storage.get_value(StorageKeys.MEDIATOR_CHAT)

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
        await send_message(fsm_storage, msg.bot, SUCCESSFUL_SEND_ANSWER_MSG)
        reply_msg = POST_SEND_MSG
        await state.set_state(MediatorStates.check_chat)
    else:
        reply_msg = ERROR_ENTERS_REPLY_MSGS.get(result)
    await send_message(fsm_storage, msg.bot, reply_msg)
