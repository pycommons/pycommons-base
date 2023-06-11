from unittest import TestCase

from pycommons.base.atomic import Atomic


class TestAtomic(TestCase):
    def test_container(self):
        container = Atomic.with_none()

        self.assertIsNone(container.get())

        mock_object1 = object()
        container.set(mock_object1)
        self.assertEqual(mock_object1, container.get())

        mock_object2 = object()
        self.assertEqual(mock_object1, container.get_and_set(mock_object2))
        self.assertEqual(mock_object2, container.get())

        mock_object3 = object()
        self.assertEqual(mock_object3, container.set_and_get(mock_object3))
        self.assertTrue(mock_object3 in container)
