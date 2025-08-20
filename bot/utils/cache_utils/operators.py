from abc import abstractmethod
import shutil
from pathlib import Path
import secrets

from aiogram import Bot
from aiogram.types import PhotoSize, Video

from bot.utils.exception import SingleUseCache
from bot.utils.message_utils.message_setting_classes import TypesMedia

from bot.configs.configs import cache_configs

from .cache_obj import CacheMediaObj, CacheObj


class CacheOperator:
    def __init__(self):
        self._data: None | CacheObj | tuple[CacheObj] = None
        self.__cache_id: int = self.__generate_cache_id()

        self._cache_path: Path = self._create_cache_dir()

    @property
    @abstractmethod
    def _cache_dir(self) -> Path:
        pass

    @staticmethod
    def __generate_cache_id():
        return secrets.randbelow(9_000_000_000) + 1_000_000_000

    def _create_cache_dir(self) -> Path:
        path: Path = self._cache_dir / str(self.__cache_id)
        path.mkdir(exist_ok=True)
        return path

    @abstractmethod
    def caching_data(self, data, *args, **kwargs) -> None:
        pass

    def get_cache(self) -> CacheObj | tuple[CacheObj] | None:
        return self._data

    def clear_cache(self) -> None:
        shutil.rmtree(self._cache_dir)


class CacheMediaOperator(CacheOperator):
    VIDEO_EXT = '.mp4'
    PHOTO_EXT = '.jpg'

    def __init__(self):
        super().__init__()

    @property
    def _cache_dir(self) -> Path:
        return cache_configs.CACHE_MEDIA_DIR

    async def __save_media_file(self, media: PhotoSize | Video, bot: Bot) -> CacheMediaObj:
        ext = ''
        file_id = media.file_id
        file = await bot.get_file(file_id)
        type_media = ''

        if isinstance(media, PhotoSize):
            ext = self.PHOTO_EXT
            type_media = TypesMedia.TYPE_PHOTO
        elif isinstance(media, Video):
            ext = self.VIDEO_EXT
            type_media = TypesMedia.TYPE_VIDEO

        destination: Path = self._cache_path / f'{file_id}{ext}'
        await bot.download_file(file.file_path, destination)

        return CacheMediaObj(destination, type_media)

    async def caching_data(self, media: PhotoSize | Video | list[PhotoSize | Video], bot: Bot=None, *args) -> None:
        """
        This func caching and saved media data
        :param bot: aiogram bot
        :param media: media for caching
        :return: None, but path and other saved in class
        """
        if self._data is not None:
            raise SingleUseCache()

        self._create_cache_dir()

        if isinstance(media, list):
            data = []
            for media_file in media:
                cache_obj = await self.__save_media_file(media_file, bot)
                data.append(cache_obj)
            self._data = tuple(data)
        else:
            self._data = await self.__save_media_file(media, bot)

        print(self._data)
