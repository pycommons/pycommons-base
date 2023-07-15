from concurrent.futures import Future, Executor

from pycommons.base.function import RunnableType
from ..executors import DirectExecutor


class ListenableFuture(Future):
    _DIRECT_EXECUTOR = DirectExecutor()

    def add_listener(self, listener: RunnableType, executor: Executor = _DIRECT_EXECUTOR) -> None:
        def _listener(_future: Future):
            executor.submit(listener)

        self.add_done_callback(_listener)
