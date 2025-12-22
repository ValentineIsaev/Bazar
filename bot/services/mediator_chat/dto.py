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
    table_id: int
    chat_id: int

    seller_user_id: int
    buyer_user_id: int
    product_id: int

    chat_name: str


@dataclass
class ChatMessage:
    chat_id: int
    table_msg_id: int

    sender_id: int

    date: str

    text: str
    media: Path = None

    is_my_message: bool = None


@dataclass
class ErrorSendMessage:
    is_error: bool
    error: str = None

