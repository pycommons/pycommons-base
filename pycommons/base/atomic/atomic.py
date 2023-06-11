from typing import TypeVar, Generic, Optional

from pycommons.base.synchronized import RLockSynchronized, synchronized
from pycommons.base.container import Container

_T = TypeVar("_T")


class Atomic(Container[_T], RLockSynchronized, Generic[_T]):
    def __init__(self, t: Optional[_T] = None):
        super().__init__(t)
        RLockSynchronized.__init__(self)

    @synchronized
    def get(self) -> Optional[_T]:
        return super().get()

    @synchronized
    def set(self, t: _T) -> None:
        super().set(t)

    @synchronized
    def set_and_get(self, t: Optional[_T]) -> Optional[_T]:
        return super().set_and_get(t)

    @synchronized
    def get_and_set(self, t: Optional[_T]) -> Optional[_T]:
        return super().get_and_set(t)
