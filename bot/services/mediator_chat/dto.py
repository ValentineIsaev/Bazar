from dataclasses import dataclass
from bot.types.storage import LocalObjPath


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
    chat_id: str

    seller_user_id: int
    buyer_user_id: int
    product_id: int

    chat_name: str

    count_update: int = None


@dataclass
class ChatMessage:
    chat_id: str

    sender_id: int

    text: str

    table_msg_id: int = None
    date: str = None
    media: tuple[LocalObjPath, ...] = None

    is_my_message: bool = None


@dataclass
class ErrorSendMessage:
    is_error: bool
    error: str = None

