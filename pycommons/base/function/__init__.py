from __future__ import annotations

from .consumer import Consumer, BiConsumer
from .function import Function
from .predicate import Predicate, BiPredicate
from .runnable import Runnable
from .supplier import Supplier, SupplierType

__all__ = [
    "BiConsumer",
    "Consumer",
    "Function",
    "Predicate",
    "Runnable",
    "Supplier",
    "BiPredicate",
    "SupplierType",
]
