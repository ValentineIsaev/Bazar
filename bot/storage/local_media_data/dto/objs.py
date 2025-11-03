from dataclasses import dataclass
from abc import ABC

from bot.constants.utils_const import TypesMedia

from .path import LocalObjPath, ObjPath

@dataclass
class Obj(ABC):
    path: ObjPath


@dataclass
class MediaLocalObj(Obj):
    path: LocalObjPath
    type_media: TypesMedia

