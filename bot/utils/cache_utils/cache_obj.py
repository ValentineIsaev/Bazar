from dataclasses import dataclass
from pathlib import Path


@dataclass
class CacheObj:
    path: Path


@dataclass
class CacheMediaObj(CacheObj):
    type_media: str