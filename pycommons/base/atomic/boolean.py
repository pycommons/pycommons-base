from __future__ import annotations

from pycommons.base.atomic.atomic import Atomic
from pycommons.base.container.boolean import BooleanContainer
from pycommons.base.synchronized import synchronized


class AtomicBoolean(BooleanContainer, Atomic[bool]):  # pylint: disable=R0901
    """
    Atomic Boolean Container that allows atomic update of the container value.
    The object is synchronized for read and write operations so that only one read/write
    happens at a time. This is ensured using re-entrant locks. Provides
    all the functionalities provided by the
    [BooleanContainer][pycommons.base.container.BooleanContainer]

    """

    @synchronized
    def true(self) -> bool:
        return super().true()

    @synchronized
    def false(self) -> bool:
        return super().false()

    @synchronized
    def compliment(self) -> bool:
        return super().compliment()

    @classmethod
    def with_true(cls) -> AtomicBoolean:
        return cls(True)

    @classmethod
    def with_false(cls) -> AtomicBoolean:
        return cls(False)

    @synchronized
    def get(self) -> bool:
        return super().get()
