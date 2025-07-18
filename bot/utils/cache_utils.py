from dataclasses import dataclass
from abc import abstractmethod
import shutil
import os
import secrets

from aiogram import Bot
from aiogram.types import PhotoSize, Video

from .exception import SingleUseCache

from bot.configs.configs import PROJECT_ROOT


@dataclass
class CacheObj:
    path: str


@dataclass
class CacheMediaObj(CacheObj):
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'

    type_media: str


class CacheOperator:
    def __init__(self):
        self.__cache_id: str = str(self.__generate_cache_id())
        self._cache_dir: str = os.path.join(self._create_cache_path(), self.__cache_id)

    @abstractmethod
    def _create_cache_path(self) -> str:
        pass

    @staticmethod
    def __generate_cache_id():
        return secrets.randbelow(9_000_000_000) + 1_000_000_000

    @abstractmethod
    def caching_data(self, data, *args, **kwargs) -> None:
        pass

    def _create_cache_dir(self):
        if not os.path.isdir(self._cache_dir):
            os.mkdir(self._cache_dir)

    def clear_cache(self) -> None:
        shutil.rmtree(self._cache_dir)

    @property
    @abstractmethod
    def data(self):
        pass


class CacheMediaOperator(CacheOperator):
    CACHE_DIR = os.path.join('cache', 'media_cache')
    VIDEO_EXT = '.mp4'
    PHOTO_EXT = '.jpg'

    def __init__(self):
        super().__init__()
        self.__media: CacheMediaObj | tuple[CacheMediaObj] | None = None

    def _create_cache_path(self) -> str:
        return os.path.join(PROJECT_ROOT, self.CACHE_DIR)

    @property
    def data(self):
        return self.__media

    async def __save_media_file(self, media: PhotoSize | Video, bot: Bot) -> CacheMediaObj:
        ext = ''
        file_id = media.file_id
        file = await bot.get_file(file_id)
        type_media = ''

        if isinstance(media, PhotoSize):
            ext = self.PHOTO_EXT
            type_media = CacheMediaObj.TYPE_PHOTO
        elif isinstance(media, Video):
            ext = self.VIDEO_EXT
            type_media = CacheMediaObj.TYPE_VIDEO

        destination = os.path.join(self._cache_dir, f'{file_id}{ext}')
        await bot.download_file(file.file_path, destination)

        return CacheMediaObj(destination, type_media)

    async def caching_data(self, media: PhotoSize | Video | list[PhotoSize | Video], bot: Bot=None, *args) -> None:
        """
        This func caching and saved media data
        :param bot: aiogram bot
        :param media: media for caching
        :return: None, but path and other saved in class
        """
        if self.__media is not None:
            raise SingleUseCache()

        self._create_cache_dir()

        if isinstance(media, list):
            self.__media = []
            for media_file in media:
                cache_obj = await self.__save_media_file(media_file, bot)
                self.__media.append(cache_obj)
        else:
            self.__media = await self.__save_media_file(media, bot)
