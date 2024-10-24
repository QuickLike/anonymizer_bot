import asyncio
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: int | float = 0.1):
        self.latency = latency
        self.album_data = {}

    async def __call__(self, handler, event: Message, data: dict[str, Any]) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        total_before = self.collect_album_messages(event)

        await asyncio.sleep(self.latency)

        total_after = len(self.album_data[event.media_group_id]['messages'])

        if total_after != total_before:
            return

        album_messages = self.album_data[event.media_group_id]['messages']
        album_messages.sort(key=lambda x: x.message_id)
        data['album'] = album_messages
        await handler(event, data)
        del self.album_data[event.media_group_id]

    def collect_album_messages(self, event: Message):
        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {'messages': []}
        self.album_data[event.media_group_id]['messages'].append(event)
        return len(self.album_data[event.media_group_id]['messages'])
