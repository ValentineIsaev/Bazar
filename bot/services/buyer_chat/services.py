from bot.managers.session_manager.session import SessionManager
from .dto import ChatMessage, Chat


class BuyerChatService:
    def __init__(self, session: SessionManager):
        self._session = session
        self._chats: list[Chat] = []

    def new_chat(self, send_msg: ChatMessage, user_id: int):
        pass

    def send_message(self, send_msg: ChatMessage, user_id: int):
        pass

    def stop_chat(self, user_id: int):
        pass

    def get_updates(self) -> tuple[Chat]:
        pass

    def get_chat_messages(self, user_id: int) -> tuple[ChatMessage]:
        pass
