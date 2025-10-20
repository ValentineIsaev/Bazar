from pathlib import Path
from dataclasses import dataclass
from abc import ABC


@dataclass
class SavedObjData(ABC):
    pass


@dataclass
class LocalSavedObjData(SavedObjData):
    pass


@dataclass
class ObjPath(ABC):
    pass

@dataclass
class LocalObjPath(ObjPath):
    pass


@dataclass
class Obj(ABC):
    pass


@dataclass
class LocalObj(Obj):
    path: Path


@dataclass
class MediaLocalSavedObjData(LocalSavedObjData):
    pass


@dataclass
class MediaLocalObj(LocalObj):
    type_media: str
