from aiogram import types, Dispatcher
import asyncio
from data import messages
import app

async def func(cq: types.CallbackQuery):
    pass


async def wrapper(cq: types.CallbackQuery):
    await asyncio.create_task(func(cq))


def register(dp: Dispatcher):
    dp.register_callback_query_handler(wrapper, lambda call: call.data.startswith("cq"))
    # dp.register_message_handler(wrapper, lambda call: call.data == "") ## strictly equals
    # dp.register_message_handler(wrapper, lambda call: call.data in ['', '', ''])
