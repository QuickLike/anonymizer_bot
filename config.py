import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

# from db import Database

dp = Dispatcher()
# db = Database()

load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = Bot(token)

ADMIN_ID = os.getenv('ADMIN_ID')
ANONIM_GROUP_ID = os.getenv('ANONIM_GROUP_ID')
FULL_DATA_GROUP_ID = os.getenv('FULL_DATA_GROUP_ID')

STATUSES = {
    0: 'Публичный',
    1: 'Аноним',
}
