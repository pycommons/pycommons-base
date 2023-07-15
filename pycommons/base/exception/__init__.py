__all__ = ["NoSuchElementError", "IllegalStateException"]


class NoSuchElementError(RuntimeError):
    """
    Raised when an object is expected to be present but is not in real. Extends RuntimeError as
    this error happens during runtime.
    """


class IllegalStateException(RuntimeError):
    """
    Runtime Error raised when the program's state is not in a expected state or the code execution
    should never have reached this state
    """
