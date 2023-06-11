from __future__ import annotations

from typing import TypeVar


class Char(int):
    """
    Defines a class to store a single character. Inherits `int` indicating, the value of
    the character object holds the Unicode codepoint within the range (0, 65536). The class
    mimics the methods provided by
    [`str`](https://docs.python.org/3/library/stdtypes.html#string-methods) like
    [`isupper`][pycommons.base.base.char.Char.isupper],
    [`isdigit`][pycommons.base.base.char.Char.isdigit]
    indicating the functionality of the `Char` class is similar to that of a String.

    References:
        https://docs.python.org/3/library/stdtypes.html#string-methods
    """

    def __new__(cls, c: CharType) -> Char:
        """
        Generates a new Char object based on the input provided to the method.

        Args:
            c: A CharType object which can be a single character String, integer or a Char object

        Raises:
            ValueError:
                1. If the input parameter to this method is None
                2. The input string contains more than 1 character
                3. The input integer is outside the Unicode character set range (0, 65536)
        """
        if c is None:
            raise ValueError("Illegal Character")

        if isinstance(c, Char):
            return super(Char, cls).__new__(cls, int(c))

        if isinstance(c, int):
            chr(c)
            return super(Char, cls).__new__(cls, c)

        c_str: str = str(c)
        if len(c_str) > 1:
            raise ValueError("Illegal Character")
        return super(Char, cls).__new__(cls, ord(c_str))

    def __str__(self) -> str:
        return chr(int(self))

    def __len__(self) -> int:
        return 1

    def __repr__(self) -> str:
        return chr(int(self))

    def __eq__(self, other: CharType) -> bool:  # type: ignore
        return int(self) == int(Char(other))

    def __gt__(self, other: CharType) -> bool:
        return int(self) > int(Char(other))

    def __ge__(self, other: CharType) -> bool:
        return int(self) >= int(Char(other))

    def __lt__(self, other: CharType) -> bool:
        return int(self) < int(Char(other))

    def __le__(self, other: CharType) -> bool:
        return int(self) <= int(Char(other))

    def __hash__(self) -> int:
        return hash(int(self))

    def isupper(self) -> bool:
        """
        Determines if the character is an uppercase letter, by converting the code point to
        str object.

        Returns:
            True if the character is an uppercase letter, False otherwise
        """
        return chr(int(self)).isupper()

    def islower(self) -> bool:
        """
        Determines if the character is a lowercase letter, by converting the code point to
        str object.

        Returns:
            True if the character is a lowercase letter, False otherwise
        """
        return chr(int(self)).islower()

    def isalpha(self) -> bool:
        """
        Determines if the character is an alphabet, by converting the code point to str object.
        Mimics the [isalpha](https://docs.python.org/3/library/stdtypes.html#str.isalpha) method
        provided by str class in Python standard library.

        Returns:
            True if the character is an alphabet, False otherwise

        References:
            https://docs.python.org/3/library/stdtypes.html#str.isalpha
        """
        return chr(int(self)).isalpha()

    def isalnum(self) -> bool:
        """
        Determines if the character is an alphabet or a digit,
        by converting the code point to str object. Mimics the
        [isalnum](https://docs.python.org/3/library/stdtypes.html#str.isalnum) method
        provided by str class in Python standard library.

        Returns:
            True if the character is an alphabet or a digit, False otherwise

        References:
            https://docs.python.org/3/library/stdtypes.html#str.isalnum
        """
        return chr(int(self)).isalnum()

    def isascii(self) -> bool:
        """
        Determines if the codepoint is in the range (0, 128), i.e. a valid ASCII character by
        converting the code point to str object. ASCII characters have code
        points in the range U+0000-U+007F. Mimics the
        [isascii](https://docs.python.org/3/library/stdtypes.html#str.isascii) method
        provided by str class of the Python standard library

        Returns:
            True if the character is a valid ASCII character, False otherwise

        References:
            https://docs.python.org/3/library/stdtypes.html#str.isascii
        """
        return chr(int(self)).isascii()

    def isdigit(self) -> bool:
        """
        Determines if the character is a digit, by converting the code point to str object.
        Mimics the [isascii](https://docs.python.org/3/library/stdtypes.html#str.isdigit) method
        provided by str class of the Python standard library

        Returns:
            True if the character is a digit, False otherwise

        References:
            https://docs.python.org/3/library/stdtypes.html#str.isdigit
        """
        return chr(int(self)).isdigit()

    def isspace(self) -> bool:
        return chr(int(self)).isspace()

    def upper(self) -> Char:
        return Char(chr(int(self)).upper())

    def lower(self) -> Char:
        return Char(chr(int(self)).lower())

    def swapcase(self) -> Char:
        return Char(chr(int(self)).swapcase())


CharType = TypeVar("CharType", Char, int, str, None)
"""
Defines the CharType object which can be any of the following, a Char, int, str or a None
"""
