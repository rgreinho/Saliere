import unittest

from saliere.core import merge_dicts


class TestCore(unittest.TestCase):
    def setUp(self):
        self.simple_dict_a = {"name": "remy", "city": "Berkeley", "age": 21}
        self.simple_dict_b = {"name": "remy", "city": "Austin"}
        self.deep_dict_a = {"users": {"remy": {"email": "remy@cisco.com", "office": "San Jose", "age": 21}}}
        self.deep_dict_b = {
            "users": {"remy": {"email": "remy@cisco.com", "office": "Austin", "position": "python master"}}}

    def test_merge_simple_simple_00(self):
        expected = {"name": "remy", "city": "Austin", "age": 21}
        actual = merge_dicts(self.simple_dict_a, self.simple_dict_b)
        self.assertEqual(expected, actual)

    def test_merge_simple_simple_01(self):
        expected = {"name": "remy", "city": "Berkeley", "age": 21}
        actual = merge_dicts(self.simple_dict_b, self.simple_dict_a)
        self.assertEqual(expected, actual)

    def test_merge_simple_deep_00(self):
        expected = {"name": "remy", "city": "Berkeley", "age": 21,
                    "users": {"remy": {"email": "remy@cisco.com", "office": "San Jose", "age": 21}}}
        actual = merge_dicts(self.simple_dict_a, self.deep_dict_a)
        self.assertEqual(expected, actual)

    def test_merge_simple_deep_01(self):
        expected = {"name": "remy", "city": "Berkeley", "age": 21,
                    "users": {"remy": {"email": "remy@cisco.com", "office": "San Jose", "age": 21}}}
        actual = merge_dicts(self.deep_dict_a, self.simple_dict_a)
        self.assertEqual(expected, actual)

    def test_merge_deep_deep_00(self):
        expected = {
            "users": {"remy": {"age": 21, "email": "remy@cisco.com", "office": "Austin", "position": "python master"}}}
        actual = merge_dicts(self.deep_dict_a, self.deep_dict_b)
        self.assertEqual(expected, actual)

    def test_merge_deep_deep_01(self):
        expected = {
            "users": {"remy": {"age": 21, "email": "remy@cisco.com", "office": "Austin", "position": "python master"}}}
        with self.assertRaises(LookupError):
            actual = merge_dicts(self.deep_dict_a, self.deep_dict_b, raise_conflicts=True)
            self.assertEqual(expected, actual)

    def test_merge_deep_deep_02(self):
        expected = {
            "users": {"remy": {"age": 21, "email": "remy@cisco.com", "office": "San Jose", "position": "python master"}}}
        actual = merge_dicts(self.deep_dict_b, self.deep_dict_a)
        self.assertEqual(expected, actual)
