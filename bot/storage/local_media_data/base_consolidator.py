from abc import abstractmethod, ABC
from typing import Any

from .dto import Obj, ObjPath, SaveDataObj
from .const import StorageType

class DataConsolidator(ABC):
    @abstractmethod
    def _download_obj(self, *objs_data: SaveDataObj, storage_type: StorageType) -> tuple[ObjPath, ...]:
        pass

    @abstractmethod
    def save_temp_obj(self, *objs_data: SaveDataObj) -> tuple[Obj, ...]:
        pass

    @abstractmethod
    def get_obj_data(self, *path: ObjPath) -> tuple[Obj, ...]:
        pass

    @abstractmethod
    def get_obj(self, *path: ObjPath) -> tuple[Any, ...]:
        pass

    @abstractmethod
    def save_perm_obj(self, objs: SaveDataObj | Obj) -> tuple[Obj, ...]:
        pass

    @abstractmethod
    def delete_obj(self, *objs_path: ObjPath) -> None:
        pass