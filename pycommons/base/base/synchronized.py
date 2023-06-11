import functools
from abc import abstractmethod, ABC
from threading import Lock, RLock
from typing import Union, TypeVar, Callable, Any

F = TypeVar("F", bound=Callable[..., Any])


class Synchronized(ABC):
    @abstractmethod
    def _sync_lock(self) -> Union[Lock, RLock]:
        ...

    @staticmethod
    def synchronized(f: F) -> Callable[..., Any]:
        @functools.wraps(f)
        def wrapped(self: Synchronized, *args: Any, **kwargs: Any) -> Any:
            with self._sync_lock():  # pylint: disable=W0212
                return f(self, *args, **kwargs)

        return wrapped


synchronized = Synchronized.synchronized


class LockSynchronized(Synchronized):
    def _sync_lock(self) -> Union[Lock, RLock]:
        return self._lock

    def __init__(self) -> None:
        self._lock = Lock()


class RLockSynchronized(Synchronized):
    def _sync_lock(self) -> Union[Lock, RLock]:
        return self._lock

    def __init__(self) -> None:
        self._lock = RLock()
