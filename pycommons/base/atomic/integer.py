from pycommons.base.atomic.atomic import Atomic
from pycommons.base.synchronized import synchronized
from pycommons.base.container import IntegerContainer


class AtomicInteger(IntegerContainer, Atomic[int]):  # pylint: disable=R0901
    @synchronized
    def add(self, val: int) -> None:
        return super().add(val)

    @synchronized
    def add_and_get(self, val: int) -> int:
        return super().add_and_get(val)

    @synchronized
    def get_and_add(self, val: int) -> int:
        return super().get_and_add(val)

    @synchronized
    def increment(self) -> None:
        return super().increment()

    @synchronized
    def increment_and_get(self) -> int:
        return super().increment_and_get()

    @synchronized
    def get_and_increment(self) -> int:
        return super().get_and_increment()

    @synchronized
    def subtract(self, val: int) -> None:
        return super().subtract(val)

    @synchronized
    def subtract_and_get(self, val: int) -> int:
        return super().subtract_and_get(val)

    @synchronized
    def get_and_subtract(self, val: int) -> int:
        return super().get_and_subtract(val)

    @synchronized
    def get(self) -> int:
        return super().get()

    @synchronized
    def __int__(self) -> int:
        return super().__int__()

    @synchronized
    def __le__(self, other: int) -> bool:
        return super().__le__(other)

    @synchronized
    def __lt__(self, other: int) -> bool:
        return super().__lt__(other)

    @synchronized
    def __ge__(self, other: int) -> bool:
        return super().__ge__(other)

    @synchronized
    def __gt__(self, other: int) -> bool:
        return super().__gt__(other)

    @synchronized
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)
