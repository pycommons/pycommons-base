from concurrent.futures import Executor, Future
from typing import ParamSpec, Callable, TypeVar

_P = ParamSpec("_P")
_T = TypeVar("_T")


class DirectExecutor(Executor):
    """
    An Executor that runs the intended job in the same thread as that of the caller.
    This is usually helpful when writing tests for background processes.
    """

    def submit(self, fn: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> Future[_T]:
        """
        Submits a callable to run.
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
        except BaseException as exc:
            _future.set_exception(exc)
        else:
            _future.set_result(result)

        return _future
