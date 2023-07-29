import threading
from unittest import TestCase

from pycommons.base.concurrent.executor import DirectExecutor


class TestDirectExecutor(TestCase):
    def test_direct_executor_executes_runnable_on_the_same_thread(self):
        def runnable():
            return threading.current_thread()

        executor = DirectExecutor.get_instance()

        future = executor.submit(runnable)

        self.assertEqual(threading.current_thread(), future.result())

    def test_direct_executor_executes_runnable_and_throws_exception_on_the_same_thread(self):
        def runnable():
            raise Exception(threading.current_thread())

        executor = DirectExecutor.get_instance()

        future = executor.submit(runnable)

        self.assertEqual(threading.current_thread(), future.exception().args[0])
