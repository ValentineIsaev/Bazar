from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chat:
    user_id: int
    is_stop: bool = False



@dataclass
class ChatMessage:
    text: str
    media: Path = None