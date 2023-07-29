from abc import ABC
from asyncio import Future
from typing import TypeVar, Generic

from ...function.function import Function

_T = TypeVar("_T")


class FutureOnDoneCallback(Function[Future, _T], ABC, Generic[_T]):  # type: ignore
    """
    A Functional Interface that can be used to register a callback using the
    Future's `add_done_callback` method
    """
