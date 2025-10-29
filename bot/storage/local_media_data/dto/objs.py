from dataclasses import dataclass
from abc import ABC

from bot.utils.message_utils import TypesMedia

from .path import LocalObjPath, ObjPath

@dataclass
class Obj(ABC):
    path: ObjPath


@dataclass
class MediaLocalObj(Obj):
    path: LocalObjPath
    type_media: TypesMedia

