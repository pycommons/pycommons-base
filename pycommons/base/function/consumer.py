from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any, Union

_T = TypeVar("_T")
_U = TypeVar("_U")


class Consumer(Generic[_T]):
    @classmethod
    def of(cls, consumer: ConsumerType[_T]) -> Consumer[_T]:
        class BasicConsumer(Consumer[_T]):
            def accept(self, value: _T) -> None:
                consumer(value)

        if isinstance(consumer, Consumer):
            return consumer
        return BasicConsumer()

    @abstractmethod
    def accept(self, value: _T) -> None:
        pass

    def and_then(self, after: Consumer[_T]) -> Consumer[_T]:
        def _impl(_t: _T) -> None:
            self.accept(_t)
            after.accept(_t)

        return Consumer.of(_impl)

    def __call__(self, t: _T, *args: Any, **kwargs: Any) -> None:
        self.accept(t)


ConsumerCallableType = Callable[[_T], None]
"""
A callable function that adheres the signature of a Consumer
"""

ConsumerType = Union[Consumer[_T], ConsumerCallableType[_T]]
"""
The generic consumer object that can be passed to the
[`Consumer.of`][pycommons.base.function.Consumer.of].
Has the references to both Consumer and the type of lambdas
that can defined for it to be called a consumer lambda.
"""


class BiConsumer(Generic[_T, _U]):
    @classmethod
    def of(cls, consumer: BiConsumerType[_T, _U]) -> BiConsumer[_T, _U]:
        class BasicBiConsumer(BiConsumer[_T, _U]):
            def accept(self, t: _T, u: _U) -> None:
                consumer(t, u)

        if isinstance(consumer, BiConsumer):
            return consumer
        return BasicBiConsumer()

    def accept(self, t: _T, u: _U) -> None:
        pass

    def and_then(self, after: BiConsumer[_T, _U]) -> BiConsumer[_T, _U]:
        def _impl(_t: _T, _u: _U) -> None:
            self.accept(_t, _u)
            after.accept(_t, _u)

        return BiConsumer.of(_impl)

    def __call__(self, t: _T, u: _U, *args: Any, **kwargs: Any) -> None:
        self.accept(t, u)


BiConsumerCallableType = Callable[[_T, _U], None]
"""
A callable function that adheres the signature of a BiConsumer
"""

BiConsumerType = Union[BiConsumer[_T, _U], BiConsumerCallableType[_T, _U]]
"""
The generic bi-consumer object that can be passed to the
[`BiConsumer.of`][pycommons.base.function.BiConsumer.of].
Has the references to both BiConsumer and the type of lambdas
that can defined for it to be called a bi-consumer lambda.
"""
