import itertools
import typing
from typing import TypeVar, Iterator, Optional

from pycommons.base.container.boolean import BooleanContainer
from pycommons.base.container.container import Container
from pycommons.base.container.integer import IntegerContainer
from pycommons.base.container.optional import OptionalContainer
from pycommons.base.function import Consumer, Predicate, Function
from pycommons.base.function.predicate import PassingPredicate
from pycommons.base.streams.stream import Stream, _R

_T = TypeVar("_T")


class IteratorStream(Stream[_T]):
    def __init__(self, iterator: Iterator[_T]):
        self._iterator: Iterator[_T] = iterator

    def filter(self, predicate: Predicate[_T]) -> Stream[_T]:
        def _filter() -> Iterator[_T]:
            for _t in self._iterator:
                if predicate(_t):
                    yield _t

        return IteratorStream(_filter())

    def map(self, mapper: Function[_T, _R]) -> Stream[_R]:
        def _map() -> Iterator[_R]:
            for _t in self._iterator:
                yield mapper.apply(_t)

        return IteratorStream(_map())

    def flat_map(self, mapper: Function[_T, Stream[_R]]) -> Stream[_R]:
        stream: Stream[_R] = IteratorStream(iter(()))

        for _t in self._iterator:
            stream = stream.chain(mapper.apply(_t))

        return stream

    def iterator(self) -> Iterator[_T]:
        return self._iterator

    def chain(self, stream: Stream[_T]) -> Stream[_T]:
        return IteratorStream(itertools.chain(self._iterator, stream.iterator()))

    def limit(self, max_size: int) -> Stream[_T]:
        _count: IntegerContainer = IntegerContainer()

        def _limiter(_c: IntegerContainer) -> bool:
            _c.increment()
            return _c > max_size

        return self.drop_while(Predicate.of(lambda t: _limiter(_count)))

    def skip(self, n: int) -> Stream[_T]:
        _count: IntegerContainer = IntegerContainer()

        def _skipper(_c: IntegerContainer) -> bool:
            _c.increment()
            return _c < n

        return self.drop_while(Predicate.of(lambda t: _skipper(_count)))

    def take_while(self, predicate: Predicate[_T]) -> Stream[_T]:
        def _filter() -> Iterator[_T]:
            for _t in self._iterator:
                if predicate.test(_t):
                    yield _t

        return IteratorStream(_filter())

    def drop_while(self, predicate: Predicate[_T]) -> Stream[_T]:
        def _filter() -> Iterator[_T]:
            for _t in self._iterator:
                if not predicate.test(_t):
                    yield _t

        return IteratorStream(_filter())

    def for_each(
        self,
        consumer: Consumer[_T],
        *,
        break_before_accept: Optional[Predicate[_T]] = None,
        break_on_accept: Optional[Predicate[_T]] = None,
        continue_before_accept: Optional[Predicate[_T]] = None,
    ) -> None:
        if break_before_accept is not None and continue_before_accept is not None:
            raise ValueError(
                "Both break_before_accept and continue_before_accept cannot be present"
            )

        for _t in self._iterator:
            if break_before_accept is not None and break_before_accept.test(_t):
                break

            if continue_before_accept is not None and continue_before_accept.test(_t):
                continue

            consumer.accept(_t)

            if break_on_accept is not None and break_on_accept.test(_t):
                break

    def peek(
        self,
        consumer: Consumer[_T],
        *,
        break_before_accept: Optional[Predicate[_T]] = None,
        break_on_accept: Optional[Predicate[_T]] = None,
        continue_before_accept: Optional[Predicate[_T]] = None,
    ) -> Stream[_T]:
        _iter_copy_container: Container[Iterator[_T]] = Container(iter(()))

        def _consumer(_t: _T, _it_copy: Container[Iterator[_T]]) -> None:
            consumer.accept(_t)
            _it_copy.set(
                itertools.chain(typing.cast(Iterator[_T], _iter_copy_container.get()), (_t,))
            )

        self.for_each(
            Consumer.of(lambda _t: _consumer(_t, _iter_copy_container)),
            break_before_accept=break_before_accept,
            break_on_accept=break_on_accept,
            continue_before_accept=continue_before_accept,
        )

        return IteratorStream(typing.cast(Iterator[_T], _iter_copy_container.get()))

    def count(self) -> int:
        stream_count: IntegerContainer = IntegerContainer()

        def _counter(_count: IntegerContainer) -> None:
            stream_count.increment()

        self.for_each(Consumer.of(lambda t: _counter(stream_count)))

        return stream_count.get()

    def any_match(self, predicate: Predicate[_T]) -> bool:
        _match: BooleanContainer = BooleanContainer.with_false()

        def _matcher(t: _T, _m: BooleanContainer) -> None:
            if predicate.test(t):
                _m.true()

        self.for_each(
            Consumer.of(lambda t: _matcher(t, _match)),
            break_on_accept=Predicate.of(lambda t: _match.get()),
        )

        return _match.get()

    def all_match(self, predicate: Predicate[_T]) -> bool:
        _match: BooleanContainer = BooleanContainer.with_true()

        def _matcher(t: _T, _m: BooleanContainer) -> None:
            if not predicate.test(t):
                _m.false()

        self.for_each(
            Consumer.of(lambda t: _matcher(t, _match)),
            break_on_accept=Predicate.of(lambda t: not _match.get()),
        )

        return _match.get()

    def none_match(self, predicate: Predicate[_T]) -> bool:
        _match: BooleanContainer = BooleanContainer.with_true()

        def _matcher(t: _T, _m: BooleanContainer) -> None:
            if predicate.test(t):
                _m.false()

        self.for_each(
            Consumer.of(lambda t: _matcher(t, _match)),
            break_on_accept=Predicate.of(lambda t: not _match.get()),
        )

        return _match.get()

    def find_first(
        self, predicate: Optional[Predicate[_T]] = None
    ) -> OptionalContainer[_T]:  # type: ignore
        if predicate is None:
            return self.find_first(PassingPredicate())

        _match: BooleanContainer = BooleanContainer.with_false()
        _found: Container[Optional[_T]] = Container.with_none()

        def _matcher(t: _T, _m: BooleanContainer, _f: Container[Optional[_T]]) -> None:
            assert predicate is not None
            if predicate.test(t):
                _m.true()
                _f.set(t)

        self.for_each(
            Consumer.of(lambda t: _matcher(t, _match, _found)),
            break_on_accept=Predicate.of(lambda t: _match.get()),
        )

        return OptionalContainer.of_nullable(_found.get())
