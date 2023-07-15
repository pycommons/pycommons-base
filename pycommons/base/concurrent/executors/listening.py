from __future__ import annotations

import sys
import typing
from abc import abstractmethod
from concurrent.futures import Executor, Future, ThreadPoolExecutor, ProcessPoolExecutor
from typing import TypeVar, Optional, Callable, Iterable, Any, Iterator

from .direct import DirectExecutor
from ..futures import ListenableFuture

_T = TypeVar("_T")
_P = TypeVar("_P")


class _DelegatedListenableFuture(ListenableFuture[_T]):
    def __init__(self, delegate: Future[_T]) -> None:
        super().__init__()
        self._delegate: Future[_T] = delegate

    def set_result(self, result: _T) -> None:
        self._delegate.set_result(result)

    def cancel(self) -> bool:
        return self._delegate.cancel()

    def cancelled(self) -> bool:
        return self._delegate.cancelled()

    def set_running_or_notify_cancel(self) -> bool:
        return self._delegate.set_running_or_notify_cancel()

    def exception(self, timeout: Optional[float] = None) -> Optional[BaseException]:
        return self._delegate.exception(timeout)

    def result(self, timeout: Optional[float] = None) -> _T:
        return self._delegate.result(timeout)

    def done(self) -> bool:
        return self._delegate.done()

    def running(self) -> bool:
        return self._delegate.done()

    def set_exception(self, exception: Optional[BaseException]) -> None:
        return self._delegate.set_exception(exception)

    def add_done_callback(self, fn: Callable[[Future[_T]], object]) -> None:
        return self._delegate.add_done_callback(fn)

    def get_state(self) -> str:
        return typing.cast(str, getattr(self._delegate, "_state"))


class ListeningExecutor(Executor):
    @classmethod
    def decorate(cls, executor: Executor) -> ListeningExecutor:
        return _DecoratedListeningExecutor(executor)

    @abstractmethod
    def submit(self, __fn: Callable[[Any], _T], *args: Any, **kwargs: Any) -> ListenableFuture[_T]:  # type: ignore
        ...  # pragma: no cover


class _DecoratedListeningExecutor(ListeningExecutor):
    def __init__(self, decorated: Executor):
        self._decorated = decorated

    def submit(self, __fn: Callable[[_P], _T], *args: Any, **kwargs: Any) -> ListenableFuture[_T]:  # type: ignore
        return _DelegatedListenableFuture(self._decorated.submit(__fn, *args, **kwargs))

    def map(
        self,
        fn: Callable[..., _T],
        *iterables: Iterable[Any],
        timeout: Optional[float] = None,
        chunksize: int = 1,
    ) -> Iterator[_T]:
        return self._decorated.map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    if sys.version_info >= (3, 9):

        def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
            return self._decorated.shutdown(wait, cancel_futures=cancel_futures)

    else:

        def shutdown(self, wait: bool = True) -> None:
            return self._decorated.shutdown(wait)


class ListeningDirectExecutor(_DecoratedListeningExecutor):
    def __new__(cls, *args: Any, **kwargs: Any) -> ListeningExecutor:
        return ListeningExecutor.decorate(DirectExecutor())


class ListeningThreadPoolExecutor(_DecoratedListeningExecutor):
    def __new__(cls, *args: Any, **kwargs: Any) -> ListeningExecutor:
        return ListeningExecutor.decorate(ThreadPoolExecutor(*args, **kwargs))


class ListeningProcessPoolExecutor(_DecoratedListeningExecutor):
    def __new__(cls, *args: Any, **kwargs: Any) -> ListeningExecutor:
        return ListeningExecutor.decorate(ProcessPoolExecutor(*args, **kwargs))
