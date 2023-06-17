from unittest import TestCase

from pycommons.base.utils.objectutils import ObjectUtils


class TestObjectUtils(TestCase):
    def test_constructor(self):
        with self.assertRaises(ValueError):
            ObjectUtils()

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

    def test_any_none_when_none_of_the_object_is_none(self):
        obj1 = object()
        obj2 = object()
        obj3 = object()
        self.assertFalse(ObjectUtils.is_any_none(obj1, obj2, obj3))
        self.assertTrue(ObjectUtils.is_any_not_none(obj1, obj2, obj3))
        self.assertTrue(ObjectUtils.is_all_not_none(obj1, obj2, obj3))

    def test_any_none_when_one_of_the_object_is_none(self):
        obj1 = object()
        obj2 = None
        self.assertTrue(ObjectUtils.is_any_none(obj1, obj2))
        self.assertTrue(ObjectUtils.is_any_not_none(obj1, obj2))

    def test_any_not_none_when_all_of_the_object_is_none(self):
        self.assertFalse(ObjectUtils.is_any_not_none(None, None, None))
        self.assertTrue(ObjectUtils.is_all_none(None, None, None))
        self.assertFalse(ObjectUtils.is_all_not_none(None, None, None))

    def test_default_if_none_when_object_is_not_none(self):
        obj = object()
        self.assertEqual(obj, ObjectUtils.default_if_none(obj, "DEFAULT"))

    def test_default_if_none_when_object_is_none(self):
        self.assertEqual("DEFAULT", ObjectUtils.default_if_none(None, "DEFAULT"))
