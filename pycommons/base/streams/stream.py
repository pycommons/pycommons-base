from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar, Iterator, Any, Optional

from pycommons.base.container.optional import OptionalContainer
from pycommons.base.function import Predicate, Function, Consumer

_T = TypeVar("_T", bound=Any)
_R = TypeVar("_R", bound=Any)


class Stream(Generic[_T]):
    @abstractmethod
    def iterator(self) -> Iterator[_T]:
        ...

    @abstractmethod
    def chain(self, stream: Stream[_T]) -> Stream[_T]:
        ...

    @abstractmethod
    def filter(self, predicate: Predicate[_T]) -> Stream[_T]:
        ...

    @abstractmethod
    def map(self, mapper: Function[_T, _R]) -> Stream[_R]:
        ...

    @abstractmethod
    def flat_map(self, mapper: Function[_T, Stream[_R]]) -> Stream[_R]:
        ...

    @abstractmethod
    def limit(self, max_size: int) -> Stream[_T]:
        ...

    @abstractmethod
    def skip(self, n: int) -> Stream[_T]:
        ...

    @abstractmethod
    def take_while(self, predicate: Predicate[_T]) -> Stream[_T]:
        ...

    @abstractmethod
    def drop_while(self, predicate: Predicate[_T]) -> Stream[_T]:
        ...

    @abstractmethod
    def for_each(
        self,
        consumer: Consumer[_T],
        *,
        break_before_accept: Optional[Predicate[_T]] = None,
        break_on_accept: Optional[Predicate[_T]] = None,
        continue_before_accept: Optional[Predicate[_T]] = None,
    ) -> None:
        ...

    @abstractmethod
    def peek(
        self,
        consumer: Consumer[_T],
        *,
        break_before_accept: Optional[Predicate[_T]] = None,
        break_on_accept: Optional[Predicate[_T]] = None,
        continue_before_accept: Optional[Predicate[_T]] = None,
    ) -> Stream[_T]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def any_match(self, predicate: Predicate[_T]) -> bool:
        ...

    @abstractmethod
    def all_match(self, predicate: Predicate[_T]) -> bool:
        ...

    @abstractmethod
    def none_match(self, predicate: Predicate[_T]) -> bool:
        ...

    @abstractmethod
    def find_first(
        self, predicate: Optional[Predicate[_T]] = None
    ) -> OptionalContainer[_T]:  # type: ignore
        ...
