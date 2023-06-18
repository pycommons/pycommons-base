from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any, Union

from pycommons.base.utils.objectutils import ObjectUtils

_T = TypeVar("_T")
_U = TypeVar("_U")


class Predicate(Generic[_T]):
    """
    A functional interface that takes a value and returns a boolean result based on some
    operation performed on the object passed. Similar to Java's Predicate.

    References:
        https://docs.oracle.com/javase/8/docs/api/java/util/function/Predicate.html
    """

    @classmethod
    def of(cls, predicate: PredicateType[_T]) -> Predicate[_T]:
        """
        If the passed argument is a callable, then wraps the callable in a Basic Predicate instance.
        If the argument is already a predicate, then the method returns the passed argument.
        Args:
            predicate: Predicate Type (Callable/Instance)

        Returns:
            Predicate Instance
        """
        ObjectUtils.require_not_none(predicate)

        class BasicPredicate(Predicate[_T]):
            def test(self, value: _T) -> bool:
                return predicate(value)

        if isinstance(predicate, Predicate):
            return predicate
        return BasicPredicate()

    @abstractmethod
    def test(self, value: _T) -> bool:
        """
        The functional interface method that takes a value and returns
        a boolean result

        Args:
            value: Value passed to the predicate

        Returns:
            A boolean result
        """

    def negate(self) -> Predicate[_T]:
        """
        Returns a predicate that results in the negation of the current predicate's
        [`test`][pycommons.base.function.Predicate.test] result. The resulting predicate
        is wrapped in a Local Anonymous Predicate object
        Returns:

        """
        return self.of(lambda _t: not self.test(_t))

    def do_and(self, predicate: Predicate[_T]) -> Predicate[_T]:
        """
        Returns a predicate that `and`s the result of the current predicate and the
        argument predicate

        Args:
            predicate: predicate

        Returns:
            A wrapped predicate whose result is an `and` operation of the current predicate
            and the argument predicate
        """
        ObjectUtils.require_not_none(predicate)
        return self.of(lambda _t: self.test(_t) and predicate.test(_t))

    def do_or(self, predicate: Predicate[_T]) -> Predicate[_T]:
        """
        Returns a predicate that `or`s the result of the current predicate and the
        argument predicate

        Args:
            predicate: predicate

        Returns:
            A wrapped predicate whose result is an `or` operation of the current predicate
            and the argument predicate
        """
        ObjectUtils.require_not_none(predicate)
        return self.of(lambda _t: self.test(_t) or predicate.test(_t))

    def __call__(self, t: _T, *args: Any, **kwargs: Any) -> bool:
        return self.test(t)


PredicateCallableType = Callable[[_T], bool]
"""
A callable function that adheres to the signature of a predicate
"""

PredicateType = Union[Predicate[_T], PredicateCallableType[_T]]
"""
The type variable that is either a callable or a Predicate type which can be passed on to the
[`Predicate.of`][pycommons.base.function.Predicate.of] to get an instance of predicate
"""


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
