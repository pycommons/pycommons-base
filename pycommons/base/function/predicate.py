from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any

from pycommons.base.utils.objectutils import ObjectUtils

_T = TypeVar("_T")
_U = TypeVar("_U")


class Predicate(Generic[_T]):
    @classmethod
    def of(cls, predicate: Callable[[_T], bool]) -> Predicate[_T]:
        ObjectUtils.require_not_none(predicate)

        class BasicPredicate(Predicate[_T]):
            def test(self, value: _T) -> bool:
                return predicate(value)

        return BasicPredicate()

    @abstractmethod
    def test(self, value: _T) -> bool:
        pass

    def negate(self) -> Predicate[_T]:
        return self.of(lambda _t: not self.test(_t))

    def do_and(self, predicate: Predicate[_T]) -> Predicate[_T]:
        return self.of(lambda _t: self.test(_t) and predicate.test(_t))

    def do_or(self, predicate: Predicate[_T]) -> Predicate[_T]:
        return self.of(lambda _t: self.test(_t) or predicate.test(_t))

    def __call__(self, t: _T, *args: Any, **kwargs: Any) -> bool:
        return self.test(t)


class BiPredicate(Generic[_T, _U]):
    @classmethod
    def of(cls, predicate: Callable[[_T, _U], bool]) -> BiPredicate[_T, _U]:
        ObjectUtils.require_not_none(predicate)

        class BasicBiPredicate(BiPredicate[_T, _U]):
            def test(self, t: _T, u: _U) -> bool:
                return predicate(t, u)

        return BasicBiPredicate()

    @abstractmethod
    def test(self, t: _T, u: _U) -> bool:
        pass

    def negate(self) -> BiPredicate[_T, _U]:
        return self.of(lambda _t, _u: not self.test(_t, _u))

    def do_and(self, predicate: BiPredicate[_T, _U]) -> BiPredicate[_T, _U]:
        return self.of(lambda _t, _u: self.test(_t, _u) and predicate.test(_t, _u))

    def do_or(self, predicate: BiPredicate[_T, _U]) -> BiPredicate[_T, _U]:
        return self.of(lambda _t, _u: self.test(_t, _u) or predicate.test(_t, _u))

    def __call__(self, t: _T, u: _U, *args: Any, **kwargs: Any) -> bool:
        return self.test(t, u)


class PassingPredicate(Predicate[_T]):
    def test(self, value: _T) -> bool:
        return True


class FailingPredicate(Predicate[_T]):
    def test(self, value: _T) -> bool:
        return False
