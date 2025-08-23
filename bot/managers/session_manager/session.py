from redis.asyncio import Redis
import dill as pickle

class UserSession:
    def __init__(self, redis: Redis, id_session: int):
        self.id = id_session
        self._redis = redis

    async def get_all_data(self) -> dict:
        all_data = await self._redis.hgetall(name=str(self.id))
        return {
            field_name: pickle.loads(value)
            for field_name, value in all_data.items()
        }

    async def get_value(self, key: str):
        data = await self._redis.hget(name=str(self.id), key=key)
        if data is not None:
            return pickle.loads(data)
        return None

    async def get_values(self, *keys: str) -> tuple:
        values = []
        for key in keys:
            value = await self.get_value(key)
            values.append(value)
        return tuple(values)

    async def set_value(self, key: str, data):
        mapping = {key: pickle.dumps(data)}
        await self._redis.hset(name=str(self.id), mapping=mapping)

    async def set_values(self, **data):
        serialized_data: dict = {}
        for key, saved_data in data.items():
            serialized_data[key] = pickle.dumps(saved_data)
        await self._redis.hset(name=str(self.id), mapping=serialized_data)


class SessionManager:
    def __init__(self, redis: Redis):
        self._redis = redis
        self._sessions: dict = {}

    def get_session(self, user_id: int) -> UserSession:
        if not user_id in self._sessions:
            self._sessions[user_id] = UserSession(self._redis, user_id)
        return self._sessions.get(user_id)