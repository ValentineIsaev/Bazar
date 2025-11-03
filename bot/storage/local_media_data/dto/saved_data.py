from dataclasses import dataclass
from abc import ABC

from bot.constants.utils_const import TypesMedia

@dataclass
class SaveDataObj(ABC):
    pass


@dataclass
class TelegramMediaSaveData(SaveDataObj):
    file_id: str
    type_media: TypesMedia
