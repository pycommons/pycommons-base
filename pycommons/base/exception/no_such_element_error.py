"""
no_such_element_error.py

Consists of an Exception "NoSuchElementError" that is raised when an
element is expected to be present (in an Optional) but is not present.
"""


class NoSuchElementError(RuntimeError):
    """
    Raised when an object is expected to be present but is not in real. Extends RuntimeError as
    this error happens during runtime.
    """
