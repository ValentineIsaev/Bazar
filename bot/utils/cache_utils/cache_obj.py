from dataclasses import dataclass


@dataclass
class CacheObj:
    path: str


@dataclass
class CacheMediaObj(CacheObj):
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'

    type_media: str