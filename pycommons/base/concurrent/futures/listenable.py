from abc import abstractmethod, ABC
from concurrent.futures import Future, Executor
from typing import TypeVar, Generic

from pycommons.base.function import RunnableType
from ..executors.direct import DirectExecutor

_T = TypeVar("_T")


class ListenableFuture(ABC, Future, Generic[_T]):
    _DIRECT_EXECUTOR = DirectExecutor()

    def add_listener(self, listener: RunnableType, executor: Executor = _DIRECT_EXECUTOR) -> None:
        def _listener(_future: Future) -> None:
            executor.submit(listener)

        self.add_done_callback(_listener)

    @abstractmethod
    def get_state(self) -> str: ...
