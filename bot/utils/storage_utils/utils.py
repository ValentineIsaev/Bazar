from bot.types.utils import InputMedia
from bot.types.storage import TelegramMediaLocalConsolidator, MediaLocalObj


def save_temp_media(media: tuple[InputMedia] | list[InputMedia],
                    consolidator: TelegramMediaLocalConsolidator) -> tuple[MediaLocalObj, ...]:
    media_objs = []

    for media_file in media:
        pass