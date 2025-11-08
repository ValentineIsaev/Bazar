import asyncio
from pathlib import Path

from aiogram import Bot

from .dto import LocalObjPath, TelegramMediaSaveData, MediaLocalObj
from .base_consolidator import DataConsolidator

from .const import EXT, StorageType, TYPE_DATA_FROM_EXT


class TelegramMediaLocalConsolidator(DataConsolidator):
    def __init__(self, bot: Bot, temp_path: Path, storage_path: Path):
        self._bot = bot

        self._temp_path = temp_path
        self._storage_path = storage_path

    async def _download_obj(self, *objs_data: TelegramMediaSaveData,
                            storage_type: StorageType) -> tuple[LocalObjPath, ...]:
        objs_path = []
        save_path = self._storage_path if storage_type == StorageType.PERMANENT else self._temp_path
        for obj in objs_data:
            destination: Path = save_path / f'{obj.file_id}{EXT[obj.type_media]}'
            objs_path.append(LocalObjPath(destination))
            file = await self._bot.get_file(obj.file_id)
            await self._bot.download(file, destination)

        return tuple(objs_path)


    async def save_temp_obj(self, *objs_data: TelegramMediaSaveData) -> tuple[LocalObjPath, ...]:
        objs_path = await self._download_obj(*objs_data, storage_type=StorageType.TEMPORARY)
        return objs_path

    async def save_perm_obj(self, objs: tuple[TelegramMediaSaveData, ...] | tuple[MediaLocalObj, ...]) -> tuple[LocalObjPath, ...]:
        if len(objs) > 0:
            if all(map(lambda x: isinstance(x, type(objs[0])), objs)):
                if isinstance(objs[0], TelegramMediaSaveData):
                    path = await self._download_obj(*objs, storage_type=StorageType.PERMANENT)
                    return path
                elif isinstance(objs[0], MediaLocalObj):
                    path = []
                    for obj in objs:
                        obj_path = obj.path.path
                        if obj_path.exists() and obj_path.is_file():
                            new_path = self._storage_path / obj_path.name
                            obj_path.replace(new_path)
                            path.append(LocalObjPath(new_path))

                    return tuple(path)

        raise ValueError('Incorrect data!')

    def get_obj(self, *path: LocalObjPath) -> None:
        return None

    def get_obj_data(self, *path: LocalObjPath) -> tuple[MediaLocalObj, ...]:
        objs = []
        for path in path:
            obj_path = path.path
            obj = None
            if obj_path.exists() and obj_path.is_file():
                obj = MediaLocalObj(path, TYPE_DATA_FROM_EXT[obj_path.suffix])
            objs.append(obj)

        return tuple(objs)

    def delete_obj(self, *objs_path: LocalObjPath) -> None:
        for path in objs_path:
            obj_path = path.path
            if obj_path.exists() and obj_path.is_file():
                obj_path.unlink()
