from typing import TypeVar, Generic, Optional

from pycommons.base.container import Container
from pycommons.base.synchronized import RLockSynchronized, synchronized

_T = TypeVar("_T")


class Atomic(Container[_T], RLockSynchronized, Generic[_T]):
    """
    Atomic mutable container, that holds a value in the object
    and only allows synchronized read and write.
    This implementation is thread-safe and can be used across multiple threads.
    If the container is used only on a single thread, consider
    using the [Container][pycommons.base.container], and it's derived classes.

    The object is held on a re-entrant lock during reads and writes
    and is unlocked after the operation is complete.

    References:
        https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicReference.html
    """

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
