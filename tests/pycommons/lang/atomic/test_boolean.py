from unittest import TestCase

from pycommons.base.atomic import AtomicBoolean


class TestAtomicBoolean(TestCase):
    def test_container(self):
        boolean_container = AtomicBoolean.with_true()
        self.assertTrue(boolean_container)

        boolean_container.compliment()
        self.assertFalse(boolean_container.get())

        boolean_container.true()
        self.assertTrue(boolean_container)

        boolean_container.false()
        self.assertFalse(boolean_container)

    def test_container_initialized_with_false(self):
        boolean_container = AtomicBoolean.with_false()
        self.assertFalse(boolean_container)
