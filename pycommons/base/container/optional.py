from __future__ import annotations

from typing import Generic, TypeVar, Any, Optional

from pycommons.base.exception import NoSuchElementError
from pycommons.base.function.consumer import Consumer
from pycommons.base.function.function import Function
from pycommons.base.function.predicate import Predicate
from pycommons.base.function.runnable import RunnableType, Runnable
from pycommons.base.function.supplier import Supplier, SupplierType
from pycommons.base.utils.objectutils import ObjectUtils

_T = TypeVar("_T", Any, None)
_U = TypeVar("_U", Any, None)
_E = TypeVar("_E", RuntimeError, Exception)


class OptionalContainer(Generic[_T]):
    """
    Identical implementation of Java's Optional.
    A container object which may or may not contain a non-null value.

    References:
        https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html
    """

    _value: _T

    def __init__(self, value: Optional[_T]):
        """
        Initialize the container with a value if present, None if not.
        Args:
            value: The initializing value. Can be None or not-None
        """
        self._value = value

    def get(self) -> _T:
        """
        Gets the value in the container

        Returns:
            the value if present

        Raises:
            NoSuchElementError if the value is not present.

        """
        if self._value is None:
            raise NoSuchElementError("No value present")
        return self._value

    def is_present(self) -> bool:
        """
        Returns True if a value is present in the container, False otherwise

        Returns:
            True if the container value is not None
        """
        return self._value is not None

    def is_empty(self) -> bool:
        """
        Returns True if the container value is None, False otherwise

        Returns:
            True if the container value is None
        """
        return not self.is_present()

    def if_present(self, consumer: Consumer[_T]) -> None:
        """
        Run a consumer if the value is present.

        Args:
            consumer: Consumer Lambda

        Returns:
            None
        """
        ObjectUtils.require_not_none(consumer)
        if self.is_present():
            consumer.accept(self._value)

    def if_present_or_else(self, consumer: Consumer[_T], runnable: RunnableType) -> None:
        """
        Runs a consumer if the value is present, else runs the runnable
        Args:
            consumer: Consumer function that runs when value is present
            runnable: Runnable function that runs when value is None

        Returns:
            None
        """
        ObjectUtils.require_not_none(consumer)
        if self.is_present():
            consumer.accept(self._value)
        else:
            Runnable.of(runnable).run()

    def filter(self, predicate: Predicate[_T]) -> OptionalContainer[_T]:
        ObjectUtils.require_not_none(predicate)
        if self.is_empty():
            return self

        return self if predicate.test(self._value) else OptionalContainer.empty()

    def map(self, mapper: Function[_T, _U]) -> OptionalContainer[_U]:
        ObjectUtils.require_not_none(mapper)
        if self.is_empty():
            return OptionalContainer.empty()

        return OptionalContainer.of_nullable(mapper.apply(self._value))

    def flat_map(self, mapper: Function[_T, OptionalContainer[_U]]) -> OptionalContainer[_U]:
        ObjectUtils.require_not_none(mapper)
        if self.is_empty():
            return OptionalContainer.empty()

        return ObjectUtils.get_not_none(mapper.apply(self._value))

    def in_turn(self, supplier: SupplierType[OptionalContainer[_T]]) -> OptionalContainer[_T]:
        if self.is_present():
            return self

        return ObjectUtils.get_not_none(Supplier.of(supplier).get())

    def or_else(self, other: _T) -> _T:
        return self._value if self.is_present() else other

    def or_else_get(self, supplier: SupplierType[_T]) -> _T:
        return self._value if self.is_present() else Supplier.of(supplier).get()

    def or_else_throw(self, supplier: Optional[SupplierType[_E]] = None) -> _T:
        if self.is_empty():
            if supplier:
                raise Supplier.of(supplier).get()
            raise NoSuchElementError("No value present")
        return self._value

    @classmethod
    def of(cls, value: _T) -> OptionalContainer[_T]:
        if value is None:
            raise TypeError("Value cannot be None")
        return cls(value)

    @classmethod
    def of_nullable(cls, value: _T) -> OptionalContainer[_T]:
        return cls(value)

    @classmethod
    def empty(cls) -> OptionalContainer[_T]:
        return cls(None)
