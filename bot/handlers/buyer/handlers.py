from aiogram.fsm.state import State, StatesGroup

from ..handlers_import import *

from bot.configs.constants import ParamFSM, UserTypes

buyer_router = Router()


class BuyerStates(StatesGroup):
    choice_catalog = State()
    catalog = State()
    buy_product = State()


@buyer_router.message(Command('catalog'))
async def send_catalog(msg: Message, state: FSMContext):
    await state.update_data(**{ParamFSM.UserData.TYPE_USER:UserTypes.BUYER})
    await msg.answer('Catalog')
