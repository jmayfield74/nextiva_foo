import unittest

from hypothesis import strategies as st
from hypothesis import given
from nextiva_foo.utils import passwords


class TestPwGen(unittest.TestCase):

    @given(st.integers(min_value=10, max_value=16),
           st.integers(min_value=16, max_value=64),
           st.integers(min_value=0, max_value=5),
           st.integers(min_value=0, max_value=5),
           st.integers(min_value=0, max_value=5))
    def test_generate(self, min_size, max_size, ints, specials, uppers):
        result = passwords.generate(
            min_chars=min_size,
            max_chars=max_size,
            integers=ints,
            specials=specials,
            uppers=uppers)
        self.assertTrue(len(result) >= min_size and len(result) <= max_size)
        self.assertEqual(
            len([i for i in result if i in passwords.INTEGER_CHARS]),
            ints)
        self.assertEqual(
            len([i for i in result if i in passwords.SPECIAL_CHARS]),
            specials)
        self.assertEqual(
            len([i for i in result if i in passwords.UPPER_CHARS]),
            uppers)

    @given(st.integers(min_value=6, max_value=16),
           st.integers(min_value=16, max_value=64),
           st.integers(min_value=0, max_value=10))
    def test_fill_length(self, min_chars, max_chars, req_chars):
        result = passwords.fill_length(min_chars, max_chars, req_chars)
        self.assertTrue(result + req_chars <= max_chars)

    @given(st.lists(st.integers(), min_size=1),
           st.integers(min_value=1, max_value=1000))
    def test_char_fetch(self, data, num):
        result = passwords.char_fetch(data, num)
        self.assertEqual(len(result), num)
        self.assertTrue(all([i in data for i in result]))
