from bot.utils.message_utils import TypesMedia
from enum import Enum

EXT = {
    TypesMedia.TYPE_VIDEO: '.mp4',
    TypesMedia.TYPE_PHOTO: '.png'
}

TYPE_DATA_FROM_EXT = {
    '.mp4': TypesMedia.TYPE_VIDEO,
    '.png': TypesMedia.TYPE_PHOTO
}

class StorageType(Enum):
    TEMPORARY = 'temp_storage'
    PERMANENT = 'permanent'
