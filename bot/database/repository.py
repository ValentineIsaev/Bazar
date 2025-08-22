from typing import TypeVar, Generic

from .models.mediator_models import ChatMediatorBase

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: T):
        self._session = session
        self._model = model

    def update(self, update_mode: T):
        pass

    def delete(self, id_model: int):
        pass

    def get_by_id(self, id_model: int) -> T:
        pass


class ProductRepository(BaseRepository):
    pass


class MediatorRepository(BaseRepository[ChatMediatorBase]):
    pass
