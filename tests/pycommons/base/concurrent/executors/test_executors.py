import threading
from typing import List
from unittest import TestCase

from pycommons.base.concurrent.executor import Executors


class TestExecutors(TestCase):
    def test_single_thread_executor(self):
        def runnable(*args):
            assert args[0] is ...
            return threading.current_thread()

        with Executors.new_single_thread_executor() as executor:
            threads: List[threading.Thread] = list(executor.map(runnable, (..., ...)))
            self.assertEqual(threads[0].ident, threads[1].ident)

    def test_direct_executor_executes_runnable_on_the_same_thread(self):
        def runnable():
            return threading.current_thread()

        with Executors.get_direct_executor() as executor:
            future = executor.submit(runnable)
            self.assertEqual(threading.current_thread(), future.result())

    def test_fixed_threadpool_executor(self):
        def runnable(*args):
            assert args[0] is ...
            return threading.current_thread()

        with Executors.new_fixed_thread_pool_executor(1) as executor:
            threads: List[threading.Thread] = list(executor.map(runnable, (..., ...)))
            self.assertEqual(threads[0].ident, threads[1].ident)
