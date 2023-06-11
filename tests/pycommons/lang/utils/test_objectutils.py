from unittest import TestCase

from pycommons.base.utils.objectutils import ObjectUtils


class TestObjectUtils(TestCase):
    def test_require_not_none_without_error(self):
        with self.assertRaises(ValueError):
            ObjectUtils.require_not_none(None)

    def test_require_not_none_with_custom_error(self):
        with self.assertRaises(TypeError):
            ObjectUtils.require_not_none(None, TypeError())

    def test_require_not_none_with_non_null_value(self):
        obj = object()
        ObjectUtils.require_not_none(obj)

    def test_get_not_none(self):
        obj = object()
        self.assertEqual(obj, ObjectUtils.get_not_none(obj))
