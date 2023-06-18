import typing

from pycommons.base.container.container import Container


class IntegerContainer(Container[int]):
    """
    A mutable container that holds an integer value. Provides the functionalities
    of Commons-Lang's MutableInt. Provides helper methods to modify the values
    by adding/subtracting another integer from the existing value.
    By default, the value is initialized to 0 if not passed during initialization.
    The class implements multiple magic methods that makes it easy to use in conditional
    expressions and other type conversions

    Warning:
        This container implementation is not thread-safe. Use
        [AtomicInteger][pycommons.base.atomic.AtomicInteger] for synchronized
        read/write operations
    """

    def __init__(self, value: int = 0):
        """
        Initialize the container with a value, zero by default

        Args:
            value: The value the container holds
        """
        super().__init__(value)

    def add(self, val: int) -> None:
        """
        Add an integer to the container value and set the result
        as the container value.

        Args:
            val: Value to be added to the container value

        Returns:
            None
        """
        self.set(self.get() + val)

    def add_and_get(self, val: int) -> int:
        """
        Add a value to the current value and get the result

        Args:
            val: The value to be added to the container value

        Returns:

        """
        return typing.cast(int, self.set_and_get(self.get() + val))

    def get_and_add(self, val: int) -> int:
        """
        Returns the current value and adds the current value with the
        value passed in the argument

        Args:
            val: The value to be added to the container value

        Returns:
            The current value before performing addition
        """
        return typing.cast(int, self.get_and_set(self.get() + val))

    def increment(self) -> None:
        """
        Increments the container value by one.

        Returns:
            None
        """
        return self.add(1)

    def increment_and_get(self) -> int:
        """
        Increments the container value by one and returns the resulting value.

        Returns:
            The container value after increment operation
        """
        return self.add_and_get(1)

    def get_and_increment(self) -> int:
        """
        Gets the current value and then increments the value by one.

        Returns:
            The container value before increment operation.
        """
        return self.get_and_add(1)

    def subtract(self, val: int) -> None:
        """
        Subtract a value from the container value

        Args:
            val: The value to be subtracted from container value

        Returns:
            None
        """
        return self.add(-val)

    def subtract_and_get(self, val: int) -> int:
        """
        Subtracts the value from container value and returns
        the resulting operation after setting it in the container.

        Args:
            val: value to be subtracted from the container value

        Returns:
            The resulting value after subtraction operation
        """
        return self.add_and_get(-val)

    def get_and_subtract(self, val: int) -> int:
        """
        Gets the current value of the container and then subtracts the value
        from the container value

        Args:
            val: The value to be subtracted from the container value

        Returns:
            The value before the subtraction operation
        """
        return self.get_and_add(-val)

    def get(self) -> int:
        """
        The current value of the container

        Returns:
            The current value of the container
        """
        return typing.cast(int, super().get())

    def __int__(self) -> int:
        return self.get()

    def __le__(self, other: int) -> bool:
        return self.get() <= other

    def __lt__(self, other: int) -> bool:
        return self.get() < other

    def __ge__(self, other: int) -> bool:
        return self.get() >= other

    def __gt__(self, other: int) -> bool:
        return self.get() > other

    def __eq__(self, other: object) -> bool:
        return self.get() == other
