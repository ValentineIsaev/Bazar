from typing import TypeVar, Generic
from abc import ABC, abstractmethod

RenderType = TypeVar('RenderType')
Error = TypeVar('Error')
class ErrorRenderer(ABC, Generic[RenderType, Error]):
    @abstractmethod
    def render_error(self, error: Error, **kwargs) -> RenderType:
        pass
