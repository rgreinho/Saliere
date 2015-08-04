import unittest

from saliere.config import Config
from saliere.core import ConfigError


class TestConfig(unittest.TestCase):

    config_file = "config.yml"
    config_string = """
    common:
        testkey: "test value"
    """

    def setUp(self):
        self.c = Config()
        self.c.load_from_string(self.config_string)

    def test_key_lookup_00(self):
        value = self.c.get_value("common:testkey")
        self.assertEqual(value, "test value")

    def test_key_lookup_01(self):
        value = self.c.get_value("common:missingkey")
        self.assertEqual(value, None)

    def test_key_lookup_02(self):
        value = self.c.get_value("common:missingkey", "missing value")
        self.assertEqual(value, "missing value")

    def test_key_lookup_03(self):
        with self.assertRaises(ConfigError):
            value = self.c.get_value(None)

    def test_load_file_00(self):
        self.assertIsNotNone(self.c.config)
