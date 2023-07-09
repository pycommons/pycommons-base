import threading
import typing
from typing import Any, Dict

from ..maps.maps import Map


class ThreadContext:
    """
    Thread Context object to store thread related context in key value format. The context values
    are not passed on to a new thread automatically when a new thread is created. The implementation
    of this class is similar to the one provided by Apache Logging's `ThreadContext`

    References:
        https://logging.apache.org/log4j/2.x/log4j-api/apidocs/org/apache/logging/log4j/ThreadContext.html
    """

    _CTX_MAP_ATTR = "__context_map__"

    @classmethod
    def __get_ctx_map(cls) -> Map[str, Any]:
        current_thread = threading.current_thread()

        try:
            _ctx_map: Any = getattr(current_thread, cls._CTX_MAP_ATTR)
            assert isinstance(_ctx_map, Map)
        except AttributeError:
            setattr(current_thread, cls._CTX_MAP_ATTR, Map())
        return typing.cast(Map[str, Any], getattr(current_thread, cls._CTX_MAP_ATTR))

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get a key from the context map
        Args:
            key: Key
            default: Default value if key is not present

        Returns:
            The value of the key from the context if found.
            Default value otherwise
        """
        return cls.__get_ctx_map().get(key, default=default)

    @classmethod
    def put(cls, key: str, value: Any) -> None:
        """
        Put a key value pair to the thread context. The key is
        overwritten if its already present

        Args:
            key: Key
            value: Value to be added to context

        Returns:
            None
        """
        cls.__get_ctx_map().put(key, value)

    @classmethod
    def put_if_none(cls, key: str, value: Any) -> None:
        """
        Put a value to the context if the value is `None` in the
        context.

        Warning:
            The presence of `None` can mean two things. It can either be that
            the key is not present in the context or the value is explicitly set to
            None

        Args:
            key: Key
            value: Value to be added if current value is None

        Returns:
            None
        """
        if cls.get(key) is None:
            cls.put(key, value)

    @classmethod
    def put_all(cls, mapping: Dict[str, Any]) -> None:
        """
        Put all the key value pairs from the mapping to the Thread Context
        Args:
            mapping: Mapping

        Returns:
            None
        """
        cls.__get_ctx_map().put_all(mapping)

    @classmethod
    def remove(cls, key: str) -> None:
        """
        Remove a single key from the Thread Context
        Args:
            key: key to be removed

        Returns:
            None
        """
        if cls.contains(key):
            cls.__get_ctx_map().remove(key)

    @classmethod
    def remove_all(cls, *keys: str) -> None:
        """
        Remove all keys from
        Args:
            *keys: Keys to be removed

        Returns:
            None
        """
        for key in set(keys):
            cls.remove(key)

    @classmethod
    def clear(cls) -> None:
        """
        Clear the Thread context. Usually used in the beginning
        of a Thread.

        Returns:
            None
        """
        cls.__get_ctx_map().clear()

    @classmethod
    def get_context(cls) -> Map[str, Any]:
        """
        Get the copy of the context map. Any changes made to this map does not impact
        the original thread context

        Returns:
            Copy of the current thread context
        """
        return cls.__get_ctx_map().copy()

    @classmethod
    def contains(cls, key: str) -> bool:
        """
        Check if a key is present in the thread context
        Args:
            key: key

        Returns:
            True if the key is present in the thread context, False otherwise
        """
        return cls.__get_ctx_map().contains_key(key)

    @classmethod
    def is_empty(cls) -> bool:
        """
        Check if the Thread Context is empty
        Returns:
            True if the context is empty, False otherwise.
        """
        return cls.__get_ctx_map().is_empty()
