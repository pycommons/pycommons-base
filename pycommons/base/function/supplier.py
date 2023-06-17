from __future__ import annotations

import typing
from abc import abstractmethod
from types import FunctionType
from typing import TypeVar, Generic, Callable, Any, Union

from pycommons.base.function.interface import FunctionalInterface

_T = TypeVar("_T")


class Supplier(FunctionalInterface, Generic[_T]):
    @classmethod
    def of(cls, supplier: SupplierType[_T]) -> Supplier[_T]:
        class BasicSupplier(Supplier[_T]):
            def get(self) -> _T:
                return supplier()

        if isinstance(supplier, FunctionType):
            return BasicSupplier()
        return typing.cast(Supplier[_T], supplier)

    @abstractmethod
    def get(self) -> _T:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        return self.get()


SupplierCallableType = Callable[[], _T]
SupplierType = Union[Supplier[_T], SupplierCallableType[_T]]
