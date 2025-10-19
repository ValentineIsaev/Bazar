from bot.managers.base import StorageManager


def require_field(field_name: str, storage_name: str):
    def decorator(method):
        async def wrapped(self: StorageManager, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None:
                value = await self._storage.get_value(storage_name)
            if value is None:
                raise TypeError(f'{field_name} is None!')

            setattr(self, field_name, value)

            return await method(self, *args, **kwargs)
        return wrapped
    return decorator