from typing import Any
from unittest import TestCase

from pycommons.base.maps import Map


class TestMap(TestCase):
    def test_map_methods(self):
        commons_map: Map[str, Any] = Map()

        self.assertTrue(commons_map.is_empty())

        commons_map.put("testKey1", "testValue1")
        self.assertFalse(commons_map.is_empty())
        self.assertEqual(1, commons_map.size())
        self.assertTrue(commons_map.contains_key("testKey1"))
        self.assertTrue(commons_map.contains_value("testValue1"))

        commons_map.put_if_absent("testKey2", "testValue2")
        self.assertEqual("testValue2", commons_map.get("testKey2"))

        commons_map.put_if_absent("testKey2", "testValue3")
        self.assertEqual("testValue2", commons_map.get("testKey2"))

        commons_map.put_entry(Map.Entry("testKey3", 3))
        self.assertEqual(3, commons_map.get("testKey3"))

        commons_map.compute_if_absent("testKey4", lambda k: 4)
        self.assertEqual(4, commons_map.get("testKey4"))

        self.assertSetEqual({"testKey1", "testKey2", "testKey3", "testKey4"}, commons_map.key_set())
        self.assertEqual(4, len(commons_map.entry_set()))

        commons_map.put_all({"testKey5": "testValue5"})
        self.assertEqual("testValue5", commons_map.remove("testKey5"))
        self.assertEqual(4, commons_map.size())
