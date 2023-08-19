from unittest import TestCase

from pycommons.base.exception import CommonsException, CommonsRuntimeException
from tests.parametrized import CommonsTestData, cases


class TestCommonsException(TestCase):

    @cases(
        CommonsTestData(data=CommonsException, expected=None),
        CommonsTestData(data=CommonsRuntimeException, expected=None)
    )
    def test_initialize_without_params(self, test_data: CommonsTestData):
        try:
            raise test_data.data()
        except test_data.data as exc:
            self.assertEqual(test_data.expected, exc.get_message())
            self.assertIsNone(exc.get_cause())
            self.assertIsNotNone(exc.get_traceback())
            exc.print_traceback()

    @cases(
        CommonsTestData(data=CommonsException, expected="Some error occurred"),
        CommonsTestData(data=CommonsRuntimeException, expected="Some error occurred")
    )
    def test_initialize_with_message(self, test_data: CommonsTestData):
        try:
            raise test_data.data(message="Some error occurred")
        except test_data.data as exc:
            self.assertEqual(test_data.expected, exc.get_message())
            self.assertIsNone(exc.get_cause())
            self.assertIsNotNone(exc.get_traceback())

    @cases(
        CommonsTestData(data=CommonsException, expected="Some error occurred"),
        CommonsTestData(data=CommonsRuntimeException, expected="Some error occurred")
    )
    def test_initialize_with_cause(self, test_data: CommonsTestData):
        _cause = Exception("cause exception")
        try:
            raise test_data.data(message="Some error occurred", cause=_cause)
        except test_data.data as exc:
            self.assertEqual(test_data.expected, exc.get_message())
            self.assertEqual(_cause, exc.get_cause())
            self.assertEqual(_cause, exc.__cause__)
            self.assertIsNotNone(exc.get_traceback())

    @cases(
        CommonsTestData(data=CommonsException, expected="Some error occurred"),
        CommonsTestData(data=CommonsRuntimeException, expected="Some error occurred")
    )
    def test_initialize_with_cause2(self, test_data: CommonsTestData):
        _cause = Exception("cause exception")
        try:
            raise test_data.data(message="Some error occurred") from _cause
        except test_data.data as exc:
            self.assertEqual(test_data.expected, exc.get_message())
            self.assertEqual(_cause, exc.get_cause())
            self.assertEqual(_cause, exc.__cause__)
            self.assertIsNotNone(exc.get_traceback())
