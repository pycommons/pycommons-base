from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any

_T = TypeVar("_T")
_U = TypeVar("_U")


class Comparator(Generic[_T, _U]):
    @classmethod
    def of(cls, comparator: Callable[[_T, _U], int]) -> Comparator[_T, _U]:
        class BasicComparator(Comparator[_T, _U]):
            def compare_to(self, t: _T, u: _U) -> int:
                return comparator(t, u)

        return BasicComparator()

    @abstractmethod
    def compare_to(self, t: _T, u: _U) -> int:
        ...

    def reversed(self) -> Comparator[_T, _U]:
        return ReverseOrderComparator(self)

    def __call__(self, t: _T, u: _U, *args: Any, **kwargs: Any) -> int:
        return self.compare_to(t, u)


class NaturalOrderComparator(Comparator[_T, _U]):
    def compare_to(self, t: _T, u: _U) -> int:
        if t < u:  # type: ignore
            return -1
        if t == u:
            return 0
        return 1


class ReverseOrderComparator(Comparator[_T, _U]):
    def __init__(self, comparator: Comparator[_T, _U]):
        self.comparator = comparator

    def compare_to(self, t: _T, u: _U) -> int:
        if t < u:  # type: ignore
            return 1
        if t == u:
            return 0
        return -1
