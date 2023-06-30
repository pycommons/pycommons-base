from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any, Union

_T = TypeVar("_T")
_U = TypeVar("_U")


class Function(Generic[_T, _U]):
    @classmethod
    def of(cls, function: FunctionType[_T, _U]) -> Function[_T, _U]:
        class BasicFunction(Function[_T, _U]):
            def apply(self, t: _T) -> _U:
                return function(t)

        if isinstance(function, Function):
            return function
        return BasicFunction()

    @abstractmethod
    def apply(self, t: _T) -> _U:
        pass

    def __call__(self, t: _T, *args: Any, **kwargs: Any) -> _U:
        return self.apply(t)


FunctionCallableType = Callable[[_T], _U]
"""
A callable function that adheres the signature of a Function
"""

FunctionType = Union[Function[_T, _U], FunctionCallableType[_T, _U]]
"""
The generic function object that can be passed to the
[`Function.of`][pycommons.base.function.Function.of].
Has the references to both Function and the type of lambdas
that can defined for it to be called a function lambda.
"""
