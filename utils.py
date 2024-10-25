import logging

from aiogram.enums import InputMediaType
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument


async def build_media_group(album: list[Message]) -> list[InputMediaPhoto | InputMediaVideo | InputMediaAudio | InputMediaDocument] | None:
    media_group = []
    for media in album:
        media_types = {
            InputMediaType.PHOTO: InputMediaPhoto,
            InputMediaType.VIDEO: InputMediaVideo,
            InputMediaType.AUDIO: InputMediaAudio,
            InputMediaType.DOCUMENT: InputMediaDocument
        }
        if media.photo:
            file_id = media.photo[-1].file_id
            media_type = InputMediaType.PHOTO
        elif media.video:
            file_id = media.video.file_id
            media_type = InputMediaType.VIDEO
        elif media.audio:
            file_id = media.audio.file_id
            media_type = InputMediaType.AUDIO
        elif media.document:
            file_id = media.document.file_id
            media_type = InputMediaType.DOCUMENT
        else:
            logging.error('Неизвестный тип Медиа!')
            return
        caption = media.caption
        caption_entities = media.caption_entities
        show_caption_above_media = media.show_caption_above_media
        has_spoiler = media.has_media_spoiler
        media_group.append(media_types[media_type](
            type=media_type,
            media=file_id,
            caption=caption,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            show_caption_above_media=show_caption_above_media
        ))
    return media_group
