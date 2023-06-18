from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Callable, Any, Union

_T = TypeVar("_T")


class Runnable:
    """
    Provides the functionalities of the Java's Runnable functional interface with the
    interface method [`run`][pycommons.base.function.Runnable.run].
    The interface can be used with the threading operations. The interface
    provides a wrapper classmethod named [`of`][pycommons.base.function.Runnable.of] that
    wraps a callable in Runnable instance.

    References:
        https://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html
    """

    @classmethod
    def of(cls, runnable: RunnableType) -> Runnable:
        """
        Wraps a callable in a BasicRunnable instance. If the passed object is a runnable, then
        the supplier is not runnable.

        Args:
            runnable: Runnable object or a callable lambda

        Returns:
            An instance of runnable.
        """

        class BasicRunnable(Runnable):
            def run(self) -> None:
                runnable()

        if isinstance(runnable, Runnable):
            return runnable
        return BasicRunnable()

    @abstractmethod
    def run(self) -> None:
        """
        Run the interface method

        Returns:
            None
        """

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.run()


RunnableCallableType = Callable[[], None]
"""
A callable function that adheres the signature of a runnable
"""

RunnableType = Union[Runnable, RunnableCallableType]
"""
The type variable that indicates a runnable type, a lambda or a runnable instance
that can be passed to the [`Runnable.of`][pycommons.base.function.Runnable.of] classmethod
"""
