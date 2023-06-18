from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any, Union

from pycommons.base.function.interface import FunctionalInterface

_T = TypeVar("_T")


class Supplier(FunctionalInterface, Generic[_T]):
    """
    A functional interface that has a method `get` that returns a value. Mirrors the Java's Supplier
    interface. A lambda or another supplier can be wrapped into a supplier by calling the
    [`of`][pycommons.base.function.Supplier.of] classmethod. The method also implements the
    `__call__` method so that an instance of supplier can be called like a function.

    References:
        https://docs.oracle.com/javase/8/docs/api/java/util/function/Supplier.html
    """

    @classmethod
    def of(cls, supplier: SupplierType[_T]) -> Supplier[_T]:
        """
        Wrap a lambda or a function in a Basic Supplier Implementation
        that just calls the mentioned lambda. If the passed object is a supplier,
        then it is returned without wrapping.
        Args:
            supplier: A supplier type object

        Returns:
            A supplier object regardless of the input.
        """

        class BasicSupplier(Supplier[_T]):
            def get(self) -> _T:
                return supplier()

        if isinstance(supplier, Supplier):
            return supplier
        return BasicSupplier()

    @abstractmethod
    def get(self) -> _T:
        """
        The interface abstract method.

        Returns:
            The supplier return object
        """

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        return self.get()


SupplierCallableType = Callable[[], _T]
"""
A callable function that adheres the signature of a supplier
"""

SupplierType = Union[Supplier[_T], SupplierCallableType[_T]]
"""
The generic supplier object that can be passed to the
[`Supplier.of`][pycommons.base.function.Supplier.of].
Has the references to both Supplier and the type of lambdas
that can defined for it to be called a supplier lambda.
"""
