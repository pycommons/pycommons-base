from __future__ import annotations

from typing import TypeVar, Generic, Any, Optional

from pycommons.base.function import Supplier

_T = TypeVar("_T")


class Container(Generic[_T], Supplier[Optional[_T]]):
    def get(self) -> Optional[_T]:
        return self._object

    def __init__(self, t: Optional[_T] = None):
        self._object: Optional[_T] = t

    def set(self, t: Optional[_T]) -> None:
        self._object = t

    def set_and_get(self, t: Optional[_T]) -> Optional[_T]:
        self.set(t)
        return self._object

    def get_and_set(self, t: Optional[_T]) -> Optional[_T]:
        old_object = self._object
        self._object = t
        return old_object

    def __contains__(self, item: _T) -> bool:
        return self._object == item

    @classmethod
    def with_none(cls) -> Container[Any]:
        return cls()
