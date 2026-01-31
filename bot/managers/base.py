from bot.storage.redis import Storage


def storage_field(field_name: str, storage_key: str):
    def decorator(method):
        async def wrapped(self: StorageManager, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None:
                value = await self._storage.get_value(storage_key)
            if value is None:
                raise TypeError(f'{field_name} is None!')

            setattr(self, field_name, value)
            res = await method(self, *args, **kwargs)
            value = getattr(self, field_name)
            await self._storage.update_value(storage_key, value)
            return res
        return wrapped
    return decorator

def set_storage_field(field_name: str, storage_key: str):
    def decorator(method):
        async def wrapped(self: StorageManager, *args, **kwargs):
            res = await method(self, *args, **kwargs)
            value = getattr(self, field_name)
            await self._storage.update_value(storage_key, value)
            return res
        return wrapped
    return decorator



class StorageManager:
    def __init__(self, session_storage: Storage):
        self._storage = session_storage
