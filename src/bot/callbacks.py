from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

import config
import asyncio
from bot import kb
from bot.bot import dp, bot
from bot.states import FSM


@dp.callback_query_handler(Text(equals=config.back, ignore_case=True), state='*')
async def go_back_to_main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
