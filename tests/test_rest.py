import json
import unittest

from hypothesis import strategies as st
from hypothesis import given
from nextiva_foo.rest import index


class TestRest(unittest.TestCase):

    def setUp(self):
        index.app.testing = True
        self.app = index.app.test_client()

    def tearDown(self):
        pass

    def test_simple_password_generation_rest(self):
        response = self.app.get('/rpc/password')
        json_data = json.loads(response.data)
        self.assertTrue("result" in json_data)
        self.assertEqual(response.status, "200 OK")

    def test_password_generation_bad_input_rest(self):
        response = self.app.get('/rpc/password?max_chars=1&min_chars=10')
        self.assertEqual(response.status, "400 BAD REQUEST")

        response = self.app.get('/rpc/password?max_chars=bad_data')
        self.assertEqual(response.status, "400 BAD REQUEST")

    @given(st.integers(min_value=10, max_value=16),
           st.integers(min_value=16, max_value=64),
           st.integers(min_value=0, max_value=5),
           st.integers(min_value=0, max_value=5),
           st.integers(min_value=0, max_value=5))
    def test_param_password_generation_rest(self, min_size, max_size, ints, specials, uppers):
        url = '/rpc/password?min_chars={}&max_chars={}&integers={}&specials={}&uppers={}'.format(
            min_size,
            max_size,
            ints,
            specials,
            uppers
        )
        response = self.app.get(url)
        self.assertEqual(response.status, "200 OK")

    def test_matrix_sort(self):
        test_data = {
            "matrix": [
                ["a", "b", "c", "d", "e"],
                ["f", "g", "h", "i", "j"],
                ["k", "l", "m", "n", "o"],
                ["p", "q", "r", "s", "t"],
                ["u", "y", "w", "x", "y"]
            ]
        }
        expected = ['a', 'b', 'c', 'd', 'e', 'j', 'o', 't', 'y', 'x', 'w', 'y', 'u', 'p', 'k', 'f', 'g', 'h', 'i', 'n', 's', 'r', 'q', 'l', 'm']
        response = self.app.post(
            '/rpc/spiral',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data["result"], expected)
        self.assertEqual(response.status, "200 OK")
