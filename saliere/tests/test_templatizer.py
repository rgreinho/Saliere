import tempfile
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import jinja2

from saliere.templatizer import Jinjanizer
from saliere.templatizer import Templatizer


class TestTemplatizer(unittest.TestCase):
    def test_jinjanize_00(self):
        """Renders a regular template.

        All the substitution variables are provided.
        """
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

    def test_jinjanize_01(self):
        """Renders a template which does not contains any variable.
        """
        # Prepare the test template
        template_str = "Saliere is the best"
        template_vars = None

        # Prepare the jinja environment
        template_loader = jinja2.FileSystemLoader("")
        jinja_env = jinja2.Environment(loader=template_loader)
        jinja_env.get_template = MagicMock(return_value=jinja_env.from_string(template_str))

        # Jinjanize the content
        jinjanized_content = Jinjanizer.jinjanize(jinja_env, "", template_vars)

        # Assert
        self.assertEqual(jinjanized_content, template_str)

    def test_jinjanize_02(self):
        """Renders Jinja template when the substitution variables where forgotten.

        If a variable does not have a substitution, it is simply deleted.,
        """
        # Prepare the test template
        template_str = "{{ formula_name }} is the best"
        template_vars = None

        # Prepare the jinja environment
        template_loader = jinja2.FileSystemLoader("")
        jinja_env = jinja2.Environment(loader=template_loader)
        jinja_env.get_template = MagicMock(return_value=jinja_env.from_string(template_str))

        # Jinjanize the content
        jinjanized_content = Jinjanizer.jinjanize(jinja_env, "", template_vars)

        # Assert
        self.assertEqual(jinjanized_content, " is the best")

    def test_copy(self):
        """Copies the template folder hierarchy without any jinja processing.
        """
        formula_name = "UnitTest"
        type = "salt-formula"
        tmp_dir = tempfile.TemporaryDirectory()
        output_dir = tmp_dir.name
        t = Templatizer(template_type=type)

        t.copy(formula_name, output_dir)

        self.assertTrue(True)

    @patch('os.path.exists', MagicMock(return_value=True))
    def test_locate_template_00(self):
        """Locates an existing template.
        """
        custom_template_location = "/home/python/test/custom_template"
        t = Templatizer(template_type=custom_template_location)
        template_location = t.locate_template()

        self.assertEqual(custom_template_location, template_location)

    @patch('os.path.exists', MagicMock(return_value=False))
    def test_locate_template_01(self):
        """Locates a template with an invalid path.
        """
        custom_template_location = "/home/python/test/custom_template"
        t = Templatizer(template_type=custom_template_location)
        template_location = t.locate_template()

        self.assertIsNone(template_location)

    def test_list_templates_00(self):
        """Lists the available templates on the system.
        """
        custom_template_list = ["project1", "custom-template", "project2"]

        with patch('os.listdir', MagicMock(return_value=custom_template_list)):
            t = Templatizer(template_path_list=["path1"])
            available_templates = t.list_templates()

        self.assertEqual(sorted(custom_template_list), available_templates)
