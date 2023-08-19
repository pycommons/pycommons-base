from concurrent.futures import ThreadPoolExecutor
from typing import Any

from .direct import DirectExecutor
from ...utils import UtilityClass


class Executors(UtilityClass):
    """
    The Executors Utility class that contains methods to create different executors.
    """

    @classmethod
    def get_direct_executor(cls) -> DirectExecutor:
        """
        Get the singleton instance of "DirectExecutor" that runs the callable
        in the same thread as the caller.

        Returns:
            The singleton instance of `DirectExecutor`
        """
        return DirectExecutor.get_instance()

    @classmethod
    def new_single_thread_executor(cls, *args: Any, **kwargs: Any) -> ThreadPoolExecutor:
        """
        A special threadpool executor where the max number of worker
        threads is 1. If multiple tasks are submitted to this executor, they are queued
        until the thread becomes idle.

        Args:
            *args: Arguments for threadpool executor
            **kwargs: Keyword Arguments for threadpool executor

        Returns:
            a new instance of `ThreadPoolExecutor` with number of threads set to 1
        """
        return cls.new_fixed_thread_pool_executor(1, *args, **kwargs)

    @classmethod
    def new_fixed_thread_pool_executor(
        cls, n_threads: int, *args: Any, **kwargs: Any
    ) -> ThreadPoolExecutor:
        """
        A fixed threadpool with number of threads set. Can be used within a context

        Args:
            n_threads: Number of worker threads
            *args: Arguments for threadpool executor
            **kwargs: Keyword Arguments for threadpool executor

        Returns:
            A new instance of threadpool executor
        """
        return ThreadPoolExecutor(n_threads, *args, **kwargs)
