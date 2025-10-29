from abc import ABC
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ObjPath(ABC):
    pass


@dataclass
class LocalObjPath(ObjPath):
    path: Path