from __future__ import annotations

from .consumer import Consumer, BiConsumer
from .function import Function
from .predicate import Predicate, BiPredicate, PredicateType, PredicateCallableType
from .runnable import Runnable, RunnableType, RunnableCallableType
from .supplier import Supplier, SupplierType, SupplierCallableType

__all__ = [
    "BiConsumer",
    "Consumer",
    "Function",
    "Predicate",
    "PredicateType",
    "PredicateCallableType",
    "Runnable",
    "Supplier",
    "BiPredicate",
    "SupplierCallableType",
    "SupplierType",
    "RunnableType",
    "RunnableCallableType",
]
