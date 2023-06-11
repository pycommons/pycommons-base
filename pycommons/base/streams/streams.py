from typing import TypeVar, Iterable

from pycommons.base.streams.iterator import IteratorStream
from pycommons.base.streams.stream import Stream

_T = TypeVar("_T")


class Streams:
    @classmethod
    def of(cls, *args: _T) -> Stream[_T]:
        return IteratorStream(iter(args))

    @classmethod
    def flat(cls, iterable: Iterable[_T]) -> Stream[_T]:
        return IteratorStream(iter(iterable))

    @classmethod
    def empty(cls) -> Stream[_T]:
        return IteratorStream(iter(()))

    @classmethod
    def of_one(cls, element: _T) -> Stream[_T]:
        return IteratorStream(iter({element}))

    @classmethod
    def of_two(cls, e1: _T, e2: _T) -> Stream[_T]:
        return IteratorStream(iter((e1, e2)))
