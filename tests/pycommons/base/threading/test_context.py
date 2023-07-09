from unittest import TestCase

from pycommons.base.threading import ThreadContext


class TestThreadContext(TestCase):
    def test_thread_context_methods(self):
        self.assertTrue(ThreadContext.is_empty())

        ThreadContext.put("testKey1", "testValue1")
        self.assertEqual("testValue1", ThreadContext.get("testKey1"))
        self.assertFalse(ThreadContext.is_empty())

        ThreadContext.put_all({"testKey2": "testValue2", "testKey3": 3})

        self.assertDictEqual(
            {"testKey1": "testValue1", "testKey2": "testValue2", "testKey3": 3},
            dict(ThreadContext.get_context()),
        )

        # Remove a key not existing
        ThreadContext.remove("testKey4")
        self.assertDictEqual(
            {"testKey1": "testValue1", "testKey2": "testValue2", "testKey3": 3},
            dict(ThreadContext.get_context()),
        )

        ThreadContext.remove("testKey3")
        self.assertDictEqual(
            {
                "testKey1": "testValue1",
                "testKey2": "testValue2",
            },
            dict(ThreadContext.get_context()),
        )
        self.assertFalse(ThreadContext.contains("testKey3"))
        self.assertTrue(ThreadContext.contains("testKey2"))

        ThreadContext.remove_all("testKey3", "testKey2")
        self.assertDictEqual(
            {
                "testKey1": "testValue1",
            },
            dict(ThreadContext.get_context()),
        )

        ThreadContext.put_if_none("testKey4", "444")
        ThreadContext.put_if_none("testKey1", "random")
        self.assertDictEqual(
            {"testKey1": "testValue1", "testKey4": "444"}, dict(ThreadContext.get_context())
        )

        ThreadContext.clear()
        self.assertTrue(ThreadContext.is_empty())
