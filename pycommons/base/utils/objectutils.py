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

    @classmethod
    def is_any_none(cls, *args: Optional[_T]) -> bool:
        return not cls.is_all_not_none(*args)

    @classmethod
    def is_any_not_none(cls, *args: Optional[_T]) -> bool:
        return cls.first_not_none(*args) is not None

    @classmethod
    def is_all_none(cls, *args: Optional[_T]) -> bool:
        return cls.first_not_none(*args) is None

    @classmethod
    def is_all_not_none(cls, *args: Optional[_T]) -> bool:
        for arg in args:
            if arg is None:
                return False
        return True

    @classmethod
    def first_not_none(cls, *args: Optional[_T]) -> Optional[_T]:
        for arg in args:
            if arg is not None:
                return arg
        return None

    @classmethod
    def default_if_none(cls, obj: Optional[_T], default: _T) -> _T:
        return default if obj is None else obj
