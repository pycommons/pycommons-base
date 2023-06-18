from __future__ import annotations

from typing import TypeVar, Generic, Any, Optional

from pycommons.base.function import Supplier

_T = TypeVar("_T")


class Container(Generic[_T], Supplier[Optional[_T]]):
    """
    Mirrors the functionalities provided by the MutableObject in the Apache Commons-Lang package.
    Holds an object if present, None if not. The read and write methods are not thread-safe
    and are supposed to be used within the same thread.

    Examples:
        ```python
        from pycommons.base.container import Container
        from pydantic import BaseModel

        class MyModel(BaseModel):
            foo: int
            bar: str

        model = MyModel(foo=2, bar="test")
        container: Container[MyModel] = Container(model)

        print(container.get())
        # MyModel(foo=2, bar='test')

        print(model in container)
        # True

        print(container.unset())
        # MyModel(foo=2, bar='test')

        print(container.get())
        # None

        print(container.set_and_get(model))
        # MyModel(foo=2, bar='test')

        print(container.get_and_set(MyModel(foo=3, bar="test2")))
        # MyModel(foo=2, bar='test')

        container.get()
        # MyModel(foo=3, bar='test2')

        ```
        This script is complete, it should run as is.

    References:
        https://commons.apache.org/proper/commons-lang/apidocs/org/apache/commons/lang3/mutable/MutableObject.html
    """

    def get(self) -> Optional[_T]:
        """
        Get the value held by the container.

        Returns:
            The object held by the container object
        """
        return self._object

    def __init__(self, t: Optional[_T] = None):
        """
        Initialize the container

        Args:
            t: value to be held by container
        """
        self._object: Optional[_T] = t

    def set(self, t: Optional[_T]) -> None:
        """
        Set the value held by the container. This removes the current
        value held by the container and holds the new value sent in
        the arguments. The reference to the old is lost after
        the execution of this method. To get the old value after setting
        a new value, use [`get_and_set`][pycommons.base.container.Container.get_and_set]

        Args:
            t: The new value

        Returns:
            None
        """
        self._object = t

    def set_and_get(self, t: Optional[_T]) -> Optional[_T]:
        self.set(t)
        return self._object

    def get_and_set(self, t: Optional[_T]) -> Optional[_T]:
        """
        Stores the current value in a temporary object, sets the new value with
        the argument sent in the methods and returns the old value.

        Args:
            t: The new value

        Returns:
            The old value of the container
        """
        old_object = self._object
        self._object = t
        return old_object

    def __contains__(self, item: _T) -> bool:
        return self._object == item

    @classmethod
    def with_none(cls) -> Container[Any]:
        return cls()
