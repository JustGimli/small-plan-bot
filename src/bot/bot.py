import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from config import tg_token, logger, REDIS_HOST, REDIS_PORT
from bot.middleware import MembershipMiddleware


bot = Bot(token=tg_token, disable_web_page_preview=True)

# Настройка Redis хранилища
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
