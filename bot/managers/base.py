from bot.storage.redis import Storage


class StorageManager:
    def __init__(self, session_storage: Storage):
        self._storage = session_storage
