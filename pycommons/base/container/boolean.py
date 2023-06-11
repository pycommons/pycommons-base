from __future__ import annotations

import typing

from pycommons.base.container.container import Container


class BooleanContainer(Container[bool]):
    def __init__(self, flag: bool = False):
        super().__init__(flag)

    def true(self) -> bool:
        return typing.cast(bool, self.set_and_get(True))

    def false(self) -> bool:
        return typing.cast(bool, self.set_and_get(False))

    def compliment(self) -> bool:
        return typing.cast(bool, self.set_and_get(not self.get()))

    @classmethod
    def with_true(cls) -> BooleanContainer:
        return cls(True)

    @classmethod
    def with_false(cls) -> BooleanContainer:
        return cls(False)

    def get(self) -> bool:
        return typing.cast(bool, super().get())

    def __bool__(self) -> bool:
        return self.get()
