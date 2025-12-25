from pathlib import Path

from .dto import ChatMessage, Chat, ErrorSendMessage

from .constants import *


class MediatorService:
    def __init__(self):
        pass

    def processing_chat_msgs(self, msgs: tuple[ChatMessage, ...], user_id: int) -> tuple[ChatMessage, ...]:
        return msgs

    def processing_send_msg(self, msg: ChatMessage) -> ErrorSendMessage:
        if len(msg.text) < 2:
            return ErrorSendMessage(True, Errors.SHORT_LEN.value)
        return ErrorSendMessage(False)

    def __generate_chat_id(self, seller_id: int, buyer_id: int, product_id: int) -> str:
        return f'{seller_id}:{product_id}:{buyer_id}'

    def start_chat(self, seller_id: int,
                   buyer_id: int,
                   product_id: int,
                   product_name: str) -> dict:
        return {
            'seller_id': seller_id,
            'buyer_id': buyer_id,
            'product_id': product_id,
            'chat_id': self.__generate_chat_id(seller_id, buyer_id, product_id),
            'chat_name': chat_name_prefix.insert(product_name)
        }


