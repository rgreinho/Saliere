import unittest
import tempfile
from unittest.mock import MagicMock

import jinja2

from saliere.templatizer import Jinjanizer
from saliere.templatizer import Templatizer


class TestTemplatizer(unittest.TestCase):
    def test_jinjanize(self):
        # Prepare the test template
        template_str = "{{ formula_name }} is the best"
        template_vars = { "formula_name": "MagickMock" }

        # Prepare the jinja environment
        template_loader = jinja2.FileSystemLoader("")
        jinja_env = jinja2.Environment(loader=template_loader)
        jinja_env.get_template = MagicMock(return_value=jinja_env.from_string(template_str))

        # Jinjanize the content
        jinjanized_content = Jinjanizer.jinjanize(jinja_env, "", template_vars)

        # Assert
        self.assertEqual(jinjanized_content, "MagickMock is the best")

    def test_copy(self):
        formula_name = "UnitTest"
        type = "salt-formula"
        tmp_dir = tempfile.TemporaryDirectory()
        output_dir = tmp_dir.name
        t = Templatizer(template_type=type)

        t.copy(formula_name, output_dir)

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
