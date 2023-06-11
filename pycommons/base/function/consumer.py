from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any

_T = TypeVar("_T")
_U = TypeVar("_U")


class Consumer(Generic[_T]):
    @classmethod
    def of(cls, consumer: Callable[[_T], None]) -> Consumer[_T]:
        class BasicConsumer(Consumer[_T]):
            def accept(self, value: _T) -> None:
                consumer(value)

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


class BiConsumer(Generic[_T, _U]):
    @classmethod
    def of(cls, consumer: Callable[[_T, _U], None]) -> BiConsumer[_T, _U]:
        class BasicBiConsumer(BiConsumer[_T, _U]):
            def accept(self, t: _T, u: _U) -> None:
                consumer(t, u)

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
