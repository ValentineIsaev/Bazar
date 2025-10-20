from abc import abstractmethod, ABC
from pathlib import Path
from typing import Any

from .dto import LocalObj, SavedObjData, Obj, ObjPath, LocalSavedObjData, LocalObjPath, MediaLocalObj, MediaLocalSavedObjData


class DataConsolidator(ABC):
    @abstractmethod
    def _download_obj(self, obj_data: SavedObjData) -> Any:
        pass

    @abstractmethod
    def save_obj(self, obj_data: SavedObjData) -> Obj:
        pass

    @abstractmethod
    def get_obj(self, path: ObjPath) -> Obj:
        pass

    @abstractmethod
    def add_obj(self, *obj: SavedObjData | Obj) -> None:
        pass

    @abstractmethod
    def delete_obj(self, obj: ObjPath) -> None:
        pass


class LocalConsolidator(DataConsolidator):
    @abstractmethod
    def _download_obj(self, obj_data: LocalSavedObjData) -> Any:
        pass

    def save_obj(self, obj_data: LocalSavedObjData) -> LocalObj:
        # Здесь будет реализация

        pass

    def add_obj(self, *obj: LocalSavedObjData | LocalObj) -> None:
        # Здесь будет реализация

        pass

    def get_obj(self, path: LocalObjPath) -> LocalObj:
        # Здесь будет реализация

        pass

    def delete_obj(self, obj: LocalObjPath) -> None:
        # Здесь будет реализация

        pass

class MediaLocalConsolidator(LocalConsolidator):
    @abstractmethod
    def _download_media(self, media_data: LocalSavedObjData) -> Path:
        pass

    def _download_obj(self, obj_data: LocalSavedObjData) -> Path:
        # Здесь будет реализация

        pass
