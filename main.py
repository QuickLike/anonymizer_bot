import asyncio
import logging
import sys

from aiogram.enums import InputMediaType
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import DeleteWebhook

from album_middleware import AlbumMiddleware
from config import dp, bot, ANONIM_GROUP_ID, FULL_DATA_GROUP_ID, DELAY_TIME, LOGGING_MESSAGE_TEXT
from states import Form
from utils import build_media_group


@dp.message(Command('start'))
async def start(message: Message):
    user_id = message.from_user.id
    logging.info(f'Пользователь с ID {user_id} запустил бота.')
    await message.answer('👤Anonymizer👤\n\nВы можете отправить сообщение, фото или видео.')


@dp.message(Form.phone_number)
async def trolling(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if chat_id == user_id:
        user_channel_status = await bot.get_chat_member(chat_id=ANONIM_GROUP_ID, user_id=user_id)
        if user_channel_status.status == 'member':
            await state.clear()
            await bot.send_message(user_id, 'Теперь вы можете писать сообщение.')
        else:
            await bot.send_message(user_id, 'Вы ввели неправильный номер!')


@dp.message()
async def message_handle(message: Message, state: FSMContext, album: list[Message] = None):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        logging.info(LOGGING_MESSAGE_TEXT.format(
            user_id=user_id,
            chat_id=chat_id,
            message_text=message.text)
        )
    except UnicodeEncodeError:
        print((logging.info(LOGGING_MESSAGE_TEXT.format(
            user_id=user_id,
            chat_id=chat_id,
            message_text=message.text)
        )))
    if chat_id == user_id:
        user_channel_status = await bot.get_chat_member(chat_id=ANONIM_GROUP_ID, user_id=user_id)
        if user_channel_status.status == 'member':
            username = message.from_user.username
            full_name = (f'ID ({user_id}) {message.from_user.first_name} {message.from_user.last_name}'.strip() +
                         (f' @{username}' if username else ''))
            if album:
                media_group = await build_media_group(album)
                await bot.send_media_group(ANONIM_GROUP_ID, media=media_group)
                await bot.send_media_group(FULL_DATA_GROUP_ID, media=media_group)
                await bot.send_message(FULL_DATA_GROUP_ID, text=full_name.strip())
                await bot.delete_messages(
                    chat_id=user_id,
                    message_ids=[msg.message_id for msg in album]
                )
            else:
                await asyncio.sleep(DELAY_TIME)
                await message.copy_to(chat_id=FULL_DATA_GROUP_ID)
                await bot.send_message(FULL_DATA_GROUP_ID, text=full_name.strip())
                await message.copy_to(chat_id=ANONIM_GROUP_ID)
                await message.delete()
        else:
            await state.set_state(Form.phone_number)
            await message.answer('Введите ваш номер телефона')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.message.middleware(AlbumMiddleware())
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
