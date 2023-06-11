import typing
from typing import TypeVar, Optional

from pycommons.base.utils.utils import UtilityClass

_T = TypeVar("_T")
_E = TypeVar("_E", Exception, RuntimeError)


class ObjectUtils(UtilityClass):
    @classmethod
    def require_not_none(cls, t: Optional[_T], e: Optional[_E] = None) -> None:
        if t is None:
            if e is None:
                raise ValueError("Object cannot be None")
            raise e

    @classmethod
    def get_not_none(cls, t: Optional[_T], e: Optional[_E] = None) -> _T:
        cls.require_not_none(t, e)
        return typing.cast(_T, t)
