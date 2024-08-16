
import os

from loguru import logger


OPENAI_API_KEY = os.environ.get('OPENAI_API_TOKEN')

OPEN_AI_MODEL = 'gpt-4o'
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
tg_token = os.environ.get('BOT_TOKEN')
