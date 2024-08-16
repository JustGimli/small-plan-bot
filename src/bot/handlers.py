
from aiogram import types
import io
import os
import config
import asyncio
from bot import kb
from bot.states import FSM, SwapState, GenerateState
from bot.bot import dp, bot
from aiogram.dispatcher.filters import Text
from utils import openai_helper, image_processor, get_img_url, delete_previous_message, loading, markdown_safe_split
from aiogram.dispatcher import FSMContext
from database import AsyncDatabaseSession, User
from aiogram.types import InputFile, ReplyKeyboardRemove


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, config.pre_start_text, reply_markup=ReplyKeyboardRemove())
