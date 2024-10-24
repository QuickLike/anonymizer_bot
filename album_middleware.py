from aiogram import BaseMiddleware


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: int | float = 0.1):
        self.latency = latency
        self.album_data = {}
