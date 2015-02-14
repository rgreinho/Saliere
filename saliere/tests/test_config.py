import unittest

from saliere.config import Config


class TestConfig(unittest.TestCase):

    config_file = """
    common:
        testkey: "test value"
    """

    def test_key_lookup_00(self):
        c = Config(self.config_file)
        value = c.get_value("common:testkey")
        self.assertEqual(value, "test value")

    def test_key_lookup_01(self):
        c = Config(self.config_file)
        value = c.get_value("common:missingkey")
        self.assertEqual(value, None)

    def test_key_lookup_02(self):
        c = Config(self.config_file)
        value = c.get_value("common:missingkey", "missing value")
        self.assertEqual(value, "missing value")