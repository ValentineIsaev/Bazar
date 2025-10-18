from dataclasses import dataclass
from pathlib import Path


# @dataclass
# class ChatContext:
#     recipients_id: int
#     recipients_role: str
#
#     senders_id: int
#     senders_role: str
#
#     chat_name: str


@dataclass
class Chat:
    chat_id: int

    f_user_id: int
    f_user_role: str

    s_user_id: int
    s_user_role: str

    chat_name: str
    is_stop: bool



@dataclass
class ChatMessage:
    senders_id: int
    senders_role: str

    recipients_id: int
    recipients_role: str

    text: str
    media: Path = None