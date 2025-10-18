import redis.asyncio as redis

from aiogram.fsm.storage.redis import RedisStorage

user_session_redis = redis.Redis(
    host='localhost',
    db=0
)

fsm_redis = redis.Redis(
    host='localhost',
    db=1
)
fsm_storage = RedisStorage(redis=fsm_redis)