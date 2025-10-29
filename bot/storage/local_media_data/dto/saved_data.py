from dataclasses import dataclass
from abc import ABC

from bot.utils.message_utils import TypesMedia

@dataclass
class SaveDataObj(ABC):
    pass


@dataclass
class TelegramMediaSaveData(SaveDataObj):
    file_id: str
    type_media: TypesMedia
