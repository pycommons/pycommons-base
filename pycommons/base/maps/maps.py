import typing
from collections import UserDict
from typing import TypeVar, Generic, Dict, Optional, Set

from pycommons.base.function import BiConsumer
from pycommons.base.function.consumer import BiConsumerType, ConsumerType, Consumer
from pycommons.base.function.function import FunctionType, Function
from pycommons.base.streams import Stream, IteratorStream

_K = TypeVar("_K")
_V = TypeVar("_V")


class Map(UserDict, Generic[_K, _V]):  # type: ignore
    """
    The custom Dictionary implementation that provides methods
    that are similar to Java's [Map](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html)
    implementation.
    """

    data: Dict[_K, _V]

    class Entry:
        """
        A dataclass that holds an entry(key, value) of a map.
        """

        def __init__(self, key: _K, value: _V):
            self._key: _K = key
            self._value: _V = value

        @property
        def key(self) -> _K:
            return self._key

        @property
        def value(self) -> _V:
            return typing.cast(_V, self._value)

        def __hash__(self) -> int:
            return hash(self.key)

    def put(self, k: _K, v: _V) -> _V:
        """
        Add a key value pair to the map
        Args:
            k: Key
            v: Value

        Returns:
            The value.
        """
        self.data[k] = v
        return self.data[k]

    def put_entry(self, entry: "Map.Entry") -> None:
        """
        Put an entry to the map
        Args:
            entry: `Map.Entry` instance that contains Key and Value

        Returns:
            None
        """
        self.put(typing.cast(_K, entry.key), typing.cast(_V, entry.value))

    def put_if_absent(self, k: _K, v: _V) -> _V:
        """
        Add a key value pair to the map only when the key is not present
        Args:
            k: Key
            v: Value

        Returns:

        """
        if k not in self.data:
            self.put(k, v)
        return self.data[k]

    def compute_if_absent(self, k: _K, function: FunctionType[_K, _V]) -> _V:
        """
        Add a key value pair by calling a function that
        returns the value based on the key passed.

        Args:
            k: key
            function: the callable that generates the value

        Returns:
            the value
        """
        self.put_if_absent(k, Function.of(function).apply(k))
        return self.data[k]

    def size(self) -> int:
        """
        Returns the size of the map

        Returns:
            the size of the map
        """
        return len(self.data)

    def is_empty(self) -> bool:
        """
        Returns True if the map is empty

        Returns:
            true if the map is empty, false otherwise
        """
        return self.size() == 0

    def contains_key(self, k: _K) -> bool:
        """
        Returns True if a particular key is present in the map.

        Args:
            k: key

        Returns:
            True if a key is present in the map, False otherwise
        """
        return k in self.data

    def contains_value(self, v: _V) -> bool:
        """
        Returns True if a particular value is present in the map.

        Args:
            v: value

        Returns:
            True if a value is present in the map, False otherwise
        """
        return v in self.data.values()

    def remove(self, k: _K) -> Optional[_V]:
        """
        Removes a key `k` from the map if its present and returns the removed value. If the key
        is not present, the method returns `None`. The return value `None`
        does not imply that the key was not present in the dictionary.
        It can also mean, the value of the key in the map was None.

        Args:
            k: key to be removed from map

        Returns:
            Value if the key is present. None, if the value is None or the
            map doesn't contain the key.
        """
        return self.data.pop(k) if k in self.data else None

    def put_all(self, m: Dict[_K, _V]) -> None:
        """
        Put all the keys from another dictionary to this map

        Args:
            m: map

        Returns:
            None
        """
        self.data.update(m)

    def key_set(self) -> Set[_K]:
        """
        Returns the set of keys in the map

        Returns:
            Set of keys
        """
        return set(self.keys())

    def entry_set(self) -> Set["Map.Entry"]:
        """
        Returns the set of `Map.Entry` in the map

        Returns:
            Set of map entries
        """
        return {Map.Entry(k, v) for k, v in self.data.items()}

    def for_each(self, bi_consumer: BiConsumerType[_K, _V]) -> None:
        """
        Runs a bi-consumer callable on each key value pairs in the map

        Args:
            bi_consumer: Callable that consumes 2 args, key and value

        Returns:
            None
        """
        _consumer: BiConsumer[_K, _V] = BiConsumer.of(bi_consumer)
        for k, v in self.data.items():
            _consumer.accept(k, v)

    def for_each_entry(self, consumer: ConsumerType["Map.Entry"]) -> None:
        """
        Runs a consumer callable on each entry(`Map.Entry`) in the map
        Args:
            consumer: Callable that consumes 1 arg, the Map.Entry object

        Returns:
            None
        """
        _consumer: Consumer[Map.Entry] = Consumer.of(consumer)
        for k, v in self.data.items():
            _consumer.accept(Map.Entry(k, v))

    def replace_old_value(self, k: _K, old_value: _V, new_value: _V) -> bool:
        """
        Replaces a key with a new value only if the `old_value` arg passed matches with the current
        value present in the map.
        Args:
            k: key
            old_value: Old value
            new_value: New value to be inserted to the map

        Returns:
            True if the value is replaced, False otherwise
        """
        _v = self.get(k)
        if _v == old_value:
            self.put(k, new_value)
            return True
        return False

    def replace(self, k: _K, v: _V) -> Optional[_V]:
        """
        Replace the key from the map if present. Returns the old value if present. The method
        will return None otherwise. The return value None does not imply that the
        key was not replaced. It can also mean that the value against that key was
        None before replacement.

        Args:
            k: key
            v: value

        Returns:
            The old value if replaced, None otherwise
        """
        if self.contains_key(k):
            _old_value = self.data[k]
            self.data[k] = v
            return _old_value
        return None

    def stream(self) -> Stream["Map.Entry"]:
        """
        Create a stream of the map entries present in the map.

        Returns:
            Stream of entries
        """
        return IteratorStream(iter(self.entry_set()))
