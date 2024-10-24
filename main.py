import asyncio
import logging
import sys

from aiogram import types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook

from config import dp, bot, ANONIM_GROUP_ID, FULL_DATA_GROUP_ID, DELAY_TIME


@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    logging.info(f'Пользователь с ID {user_id} запустил бота.')
    await message.answer('👤Anonymizer👤\n\nВы можете отправить сообщение, фото или видео.')


@dp.message()
async def message_handle(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logging.info(f'Сообщение от пользователя с ID {user_id} из чата с ID {chat_id}. {message.text}')
    if chat_id == user_id:
        user_channel_status = await bot.get_chat_member(chat_id=ANONIM_GROUP_ID, user_id=user_id)
        if user_channel_status['status'] == 'member':
            username = message.from_user.username
            full_name = (f'ID ({user_id}) {message.from_user.first_name} {message.from_user.last_name}'.strip() +
                         (f' @{username}' if username else ''))
            await asyncio.sleep(DELAY_TIME)
            await message.copy_to(chat_id=FULL_DATA_GROUP_ID)
            await bot.send_message(FULL_DATA_GROUP_ID, text=full_name.strip())
            await message.copy_to(chat_id=ANONIM_GROUP_ID)
            await message.delete()
        else:
            #  Введите номер телефона
            pass


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=('%(asctime)s, '
                '%(levelname)s, '
                '%(funcName)s, '
                '%(message)s'
                ),
        encoding='UTF-8',
        handlers=[logging.FileHandler(__file__ + '.log'),
                  logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(main())
