from concurrent.futures import Future
from unittest import TestCase

from pycommons.base.concurrent.executor import DirectExecutor
from pycommons.base.concurrent.future import FutureOnDoneCallback


class TestFutureOnDoneCallback(TestCase):
    class CallbackFixture(FutureOnDoneCallback[None]):
        def apply(self, t: Future) -> None:
            assert True is t.result()

    def test_callback(self):
        DirectExecutor.get_instance().submit(lambda: True).add_done_callback(self.CallbackFixture())
