from __future__ import annotations

import typing

from pycommons.base.container.container import Container


class BooleanContainer(Container[bool]):
    """
    A mutable container extends the [Container][pycommons.base.container.Container] and stores
    a boolean value. Custom helper methods are provided in the class to manipulate
    with the value present in the container. If the value of the boolean is not passed during
    initialization, it is set to `False` by default.

    The class also implements the `__bool__` magic method, so that the container object can directly
    be used in the conditional expressions.

    Warning:
        This class is not thread safe. If you need a thread safe BooleanContainer, checkout
        [AtomicBoolean][pycommons.base.atomic.AtomicBoolean]

    Examples:
        ```python
        from pycommons.base.container import BooleanContainer

        boolean_container = BooleanContainer.with_true()

        assert boolean_container.get()
        assert bool(boolean_container)

        boolean_container.false()

        assert boolean_container.get() is False
        assert boolean_container.compliment()
        ```
        This script is complete, it should run as is.

    References:
        https://commons.apache.org/proper/commons-lang/apidocs/org/apache/commons/lang3/mutable/MutableBoolean.html
    """

    def __init__(self, flag: bool = False):
        """
        Initialize the container with a value, False by default
        Args:
            flag: value of the container
        """
        super().__init__(flag)

    def true(self) -> bool:
        """
        Set the value of the container to `True` regardless
        of the previous value.
        Returns:
            True
        """
        return typing.cast(bool, self.set_and_get(True))

    def false(self) -> bool:
        """
        Set the value of the container to `False` regardless
        of the previous value.

        Returns:
            False
        """
        return typing.cast(bool, self.set_and_get(False))

    def compliment(self) -> bool:
        """
        Compliment the current value present in the container. If the value
        of the container is True, the container value is set to False and False is returned
        and vice-versa
        Returns:

        """
        return typing.cast(bool, self.set_and_get(not self.get()))

    @classmethod
    def with_true(cls) -> BooleanContainer:
        """
        Class method to initialize a new BooleanContainer with the value `True`.

        Returns:
            A new container with value set to `True`
        """
        return cls(True)

    @classmethod
    def with_false(cls) -> BooleanContainer:
        """
        Class method to initialize a new BooleanContainer with the value `False`.

        Returns:
            A new container with value set to `False`
        """
        return cls(False)

    def get(self) -> bool:
        """
        Gets the value in the container.

        Returns:
            The boolean value in the container.
        """
        return typing.cast(bool, super().get())

    def __bool__(self) -> bool:
        return self.get()
