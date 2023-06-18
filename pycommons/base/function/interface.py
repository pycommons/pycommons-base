from abc import ABC, abstractmethod
from typing import TypeVar, Any


class FunctionalInterface(ABC):
    __TYPE__: TypeVar

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...
