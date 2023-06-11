from unittest import TestCase

from mockito import mock, when, verify, unstub, ANY, forget_invocations

from pycommons.base.container.optional import OptionalContainer
from pycommons.base.exception import NoSuchElementError
from pycommons.base.function import Consumer, Runnable


class TestOptionalContainer(TestCase):
    def test_container(self):
        optional_bool: OptionalContainer[bool] = OptionalContainer.of(True)

        self.assertTrue(optional_bool.is_present())
        self.assertFalse(optional_bool.is_empty())
        self.assertTrue(optional_bool.get())

        mock_object = mock()
        when(mock_object).when_present(ANY(bool)).thenReturn("ok")
        when(mock_object).when_absent().thenReturn("ok")

        optional_bool.if_present(Consumer.of(mock_object.when_present))
        verify(mock_object, times=1).when_present(ANY(bool))
        forget_invocations(mock_object)

        optional_bool.if_present_or_else(
            Consumer.of(mock_object.when_present), Runnable.of(mock_object.when_absent)
        )
        verify(mock_object, times=1).when_present(ANY(bool))
        verify(mock_object, times=0).when_absent()

    def test_container_without_value(self):
        optional_bool: OptionalContainer[bool] = OptionalContainer.empty()

        self.assertFalse(optional_bool.is_present())
        self.assertTrue(optional_bool.is_empty())
        with self.assertRaises(NoSuchElementError):
            optional_bool.get()

        mock_object = mock()
        when(mock_object).when_present(ANY(bool)).thenReturn("ok")
        when(mock_object).when_absent().thenReturn("ok")

        optional_bool.if_present(Consumer.of(mock_object.test_method))
        verify(mock_object, times=0).test_method(ANY(bool))
        forget_invocations(mock_object)

        optional_bool.if_present_or_else(
            Consumer.of(mock_object.when_present), Runnable.of(mock_object.when_absent)
        )
        verify(mock_object, times=0).when_present(ANY(bool))
        verify(mock_object, times=1).when_absent()

    def tearDown(self) -> None:
        unstub()
