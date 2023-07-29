from __future__ import annotations

from concurrent.futures import Executor, Future
from typing import Callable, TypeVar, Any, ClassVar

_P = TypeVar("_P")
_T = TypeVar("_T")


class DirectExecutor(Executor):
    """
    An Executor that runs the intended job in the same thread as that of the caller.
    This is usually helpful when writing tests for background processes.
    """

    __instance__: ClassVar[DirectExecutor]
    """
    A class instance of the direct executor which can be used everywhere
    for executing a task in the same thread as that of the caller.
    """

    @classmethod
    def get_instance(cls) -> DirectExecutor:
        """
        Gets the singleton instance of `DirectExecutor`

        Returns:
            The singleton instance of `DirectExecutor`
        """
        return cls.__instance__

    def submit(  # pylint: disable=W0221
        self, fn: Callable[[Any], _T], *args: Any, **kwargs: Any
    ) -> Future[_T]:  # pylint: disable=W0221
        """
        Submits a callable to run in the same thread as the caller.

        Args:
            fn: The callable
            *args: Arguments of the callable
            **kwargs: Keyword args of the callable

        Returns:
            Future object
        """
        _future: Future[_T] = Future()

        try:
            result: _T = fn(*args, **kwargs)
        except BaseException as exc:  # pylint: disable=W0718
            _future.set_exception(exc)
        else:
            _future.set_result(result)

        return _future


DirectExecutor.__instance__ = DirectExecutor()
