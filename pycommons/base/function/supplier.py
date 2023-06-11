from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any

_T = TypeVar("_T")


class Supplier(Generic[_T]):
    @classmethod
    def of(cls, supplier: Callable[[], _T]) -> Supplier[_T]:
        class BasicSupplier(Supplier[_T]):
            def get(self) -> _T:
                return supplier()

        return BasicSupplier()

    @abstractmethod
    def get(self) -> _T:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        return self.get()
