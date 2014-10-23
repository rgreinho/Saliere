import unittest
import tempfile
from unittest.mock import MagicMock

import jinja2

from saliere.saliere import jinjanize
from saliere.saliere import process


class TestJinjan(unittest.TestCase):
    def test_jinjanize(self):
        # Prepare the test template
        template_str = "{{ formula_name }} is the best"

        # Prepare the jinja environment
        template_loader = jinja2.FileSystemLoader("")
        jinja_env = jinja2.Environment(loader=template_loader)
        jinja_env.get_template = MagicMock(return_value=jinja_env.from_string(template_str))

        # Jinjanize the content
        jinjanized_content = jinjanize(jinja_env, "", "MagickMock")

        # Assert
        self.assertEqual(jinjanized_content, "MagickMock is the best")


class TestProcess(unittest.TestCase):
    def test_process(self):
        formula_name = "UnitTest"
        template = "template-formula"
        tmp_dir = tempfile.TemporaryDirectory()
        output_dir = tmp_dir.name

        process(template, formula_name, output_dir)

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
