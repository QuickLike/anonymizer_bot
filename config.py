import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv


load_dotenv()
dp = Dispatcher()
bot = Bot(os.getenv('BOT_TOKEN'))

ANONIM_GROUP_ID = os.getenv('ANONIM_GROUP_ID')
FULL_DATA_GROUP_ID = os.getenv('FULL_DATA_GROUP_ID')

DELAY_TIME = 2

LOGGING_MESSAGE_TEXT = 'Сообщение от пользователя с ID {user_id} из чата с ID {chat_id}. {message_text}'
