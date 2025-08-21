from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: T):
        self._session = session
        self._model = model


class ProductRepository(BaseRepository):
    pass


class MediatorRepository(BaseRepository):
    pass
