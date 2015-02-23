import unittest

from saliere.config import Config


class TestConfig(unittest.TestCase):

    config_file = "config.yml"
    config_string = """
    common:
        testkey: "test value"
    """

    def test_key_lookup_00(self):
        c = Config()
        c.load_from_string(self.config_string)
        value = c.get_value("common:testkey")
        self.assertEqual(value, "test value")

    def test_key_lookup_01(self):
        c = Config()
        c.load_from_string(self.config_string)
        value = c.get_value("common:missingkey")
        self.assertEqual(value, None)

    def test_key_lookup_02(self):
        c = Config()
        c.load_from_string(self.config_string)
        value = c.get_value("common:missingkey", "missing value")
        self.assertEqual(value, "missing value")

    def test_load_file_00(self):
        c = Config()
        c.load_from_file(self.config_file)
        self.assertIsNotNone(c.config)
