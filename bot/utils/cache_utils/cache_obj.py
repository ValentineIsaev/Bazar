from dataclasses import dataclass
from pathlib import Path


@dataclass
class CacheObj:
    path: Path


@dataclass
class CacheMediaObj(CacheObj):
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'

    type_media: str