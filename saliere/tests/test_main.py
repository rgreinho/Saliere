import unittest

from saliere.main import load_variables


class TestMain(unittest.TestCase):
    def setUp(self):
        self.correct_string_single_var = "var1=value1"
        self.correct_string_multiple_vars = "var1=value1|var2=value2"
        self.incorrect_string = "var1=value1,var2=value2"
        self.correct_yaml = """
        {
            'vagrant-ansible': {
                'vm': {
                    'forwarded_ports': {
                        8000: 8000,
                        8888: 8888
                    },
                    'memory_size': 8192,
                    'name': 'vagrant-rally',
                    'synced_folders': {
                        '/opt/devstack': '~/projects/devstack',
                        '/opt/scripts': '~/projects/engineering/scripts'
                    }
                }
            }
        }
        """

    def test_load_variables_correct_string_00(self):
        """Loads a correct string of variables"""
        var_dict = load_variables(self.correct_string_single_var)
        self.assertIsNotNone(var_dict)
        self.assertEqual(len(var_dict), 1)

    def test_load_variables_correct_string_01(self):
        """Loads a correct string of variables"""
        var_dict = load_variables(self.correct_string_multiple_vars)
        self.assertIsNotNone(var_dict)
        self.assertEqual(len(var_dict), 2)

    def test_load_variables_incorrect_string_00(self):
        """Loads a incorrect string of variables"""
        var_dict = load_variables(self.incorrect_string)
        self.assertIsNotNone(var_dict)

    def test_load_variables_correct_yaml(self):
        """Loads a correct yaml"""
        var_dict = load_variables(self.correct_yaml)
        self.assertIsNotNone(var_dict)
        self.assertIsInstance(var_dict, dict)
