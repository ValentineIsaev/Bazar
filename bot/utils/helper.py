from aiogram.fsm.context import FSMContext
import asyncio

async def get_data_state(state: FSMContext, *key_states):
    # tasks = [state.get_value(key) for key in key_states]
    # results = await asyncio.gather(*tasks)
    # print(results)
    # return tuple(results)
    user_data = await state.get_data()
    return tuple(user_data.get(key) for key in key_states)
