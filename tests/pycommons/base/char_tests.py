from unittest import TestCase

from pycommons.base.char import Char


class CharTest(TestCase):
    def test_new_character_with_str(self):
        c: Char = Char("a")
        self.assertIsNotNone(c)
        self.assertEqual("a", str(c))
        self.assertEqual("a", chr(c))
        self.assertEqual("a", repr(c))

        self.assertEqual(1, len(c))
        self.assertTrue(c < "b")
        self.assertTrue(c > "A")
        self.assertTrue(c <= "a")
        self.assertTrue(c >= "a")

        self.assertEqual("A", c.upper())
        self.assertEqual("a", c.lower())
        self.assertEqual("A", c.swapcase())
        self.assertTrue(c.islower())
        self.assertFalse(c.isupper())
        self.assertTrue(c.isalpha())
        self.assertTrue(c.isalnum())
        self.assertFalse(c.isdigit())
        self.assertTrue(c.isascii())
        self.assertFalse(c.isspace())

    def test_new_character_with_int(self):
        c: Char = Char(97)
        self.assertIsNotNone(c)
        self.assertEqual("a", str(c))
        self.assertEqual("a", chr(c))

    def test_new_character_with_Char(self):
        c: Char = Char(Char(97))
        self.assertIsNotNone(c)
        self.assertEqual("a", str(c))
        self.assertEqual("a", chr(c))

    def test_new_character_with_invalid_string(self):
        with self.assertRaises(ValueError):
            Char("ab")

    def test_new_character_with_invalid_int(self):
        with self.assertRaises(ValueError):
            Char(-1)
