from dataclasses import dataclass

@dataclass
class UserSession:
    user_id: int
    chat_id: int


class SessionManager:
    def __init__(self):
        pass

    def create_session(self):
        pass

    def get_session(self, user_id: int) -> UserSession:
        pass