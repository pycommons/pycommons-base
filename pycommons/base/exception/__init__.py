__all__ = [
    "CommonsException",
    "CommonsRuntimeException",
    "NoSuchElementError",
    "IllegalStateException",
]

import traceback
from types import TracebackType
from typing import Optional, Any


class CommonsException(Exception):
    def __init__(  # pylint: disable=W1113
        self, message: Optional[str] = None, cause: Optional[Exception] = None, *args: Any
    ) -> None:
        super().__init__(*args)
        if cause is not None:
            self.__cause__ = cause
        self._message = message

    def get_cause(self) -> Optional[BaseException]:
        return self.__cause__

    def get_traceback(self) -> Optional[TracebackType]:
        return self.__traceback__

    def get_message(self) -> Optional[str]:
        return self._message

    def print_traceback(self) -> None:
        traceback.print_tb(self.get_traceback())


class CommonsRuntimeException(RuntimeError):
    def __init__(  # pylint: disable=W1113
        self, message: Optional[str] = None, cause: Optional[Exception] = None, *args: Any
    ) -> None:
        super().__init__(*args)
        if cause is not None:
            self.__cause__ = cause
        self._message = message

    def get_cause(self) -> Optional[BaseException]:
        return self.__cause__

    def get_traceback(self) -> Optional[TracebackType]:
        return self.__traceback__

    def get_message(self) -> Optional[str]:
        return self._message

    def print_traceback(self) -> None:
        traceback.print_tb(self.get_traceback())


class NoSuchElementError(CommonsRuntimeException):
    """
    Raised when an object is expected to be present but is not in real. Extends RuntimeError as
    this error happens during runtime.
    """


class IllegalStateException(CommonsRuntimeException):
    """
    Runtime Error raised when the program's state is not in an expected state or the code execution
    should never have reached this state
    """
