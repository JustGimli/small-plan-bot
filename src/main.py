import os
from dotenv import load_dotenv

# from openai import OpenAI
environment = os.getenv('ENVIRONMENT', 'dev')


if environment == 'prod':
    load_dotenv('.env')
else:
    load_dotenv('.env.dev')

# from utils.upgrade_db import *
from aiogram import executor
from bot import dp


def main():
    executor.start_polling(dp, skip_updates=True)

main()
