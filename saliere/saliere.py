#!/usr/bin/python3
"""Creates a skeleton for various projects based on Jinja2 templates.

Example:

    $ saliere.py mysql -t salt-formula
    $ saliere.py mysql-django -t django
    $ saliere.py mysql -t salt-formula -o my-formula-directory
    $ saliere.py mysql -t ~/my/custom/template -o my-template-directory
"""

import argparse
from datetime import date
import os

import jinja2

# Define a list of valid paths to look for the templates
template_path_list = ['../templates', '/usr/local/share/saliere/templates']


def create_folder(folder, on_failure=None):
    """Creates a folder and the parent directories if needed.

    :param folder: name/path of the folder to create
    :param on_failure: function to execute in case of failure
    """
    try:
        os.makedirs(folder)
    except OSError:
        if on_failure:
            on_failure()


def process(template_path, formula_name, output_dir):
    """Creates the skeleton based on the chosen template.

    :param template_path: the path of the template to use
    :param formula_name: the name of the formula
    :param output_dir: the path of the output directory
    """
    # Ensure the template path ends with a "/".
    template_folder_parent = os.path.abspath(os.path.dirname(template_path)) + "/"

    # Prepare the output directory
    output_folder_root = os.path.abspath(output_dir)

    # List of the files in the template folder
    for root, subfolders, files in os.walk(template_path):
        # Prepare the jinja environment
        template_loader = jinja2.FileSystemLoader(root)
        jinja_env = jinja2.Environment(loader=template_loader)

        # Recreate the folders with the formula name
        template_folder_base = root.replace(template_folder_parent, "")
        formula_folder_name = template_folder_base.replace("template", formula_name)
        formula_folder_path = os.path.join(output_folder_root, formula_folder_name)
        create_folder(formula_folder_path)

        # List the files
        for file in files:
            file_name = os.path.join(formula_folder_path, file)
            print("# Jinjanizing {0}...".format(file_name))

            # Jinjanize them
            jinjanized_content = jinjanize(jinja_env, file, formula_name)

            # Create the file with the rendered content
            with open(file_name, mode='w', encoding='utf-8') as jinjanized_file:
                jinjanized_file.write(jinjanized_content)


def jinjanize(jinja_env, template_file, formula_name):
    """Renders a Jinja2 template.

    :param jinja_env: the jinja environment
    :param template_file: the full path of the template file to render
    :param formula_name: the name of the formula
    :return: a string representing the rendered template
    """
    # Load the template
    template = jinja_env.get_template(template_file)

    # Look for the values to replace
    template_vars = {
        "formula_name": formula_name,
        "today": date.today().isoformat()
    }

    # Render the template and return the result
    return template.render(template_vars)


class Templatizer:

    def __init__(self, template_path_list=[]):
        """Initializer.

        :param template_path_list: the list of paths where the templates are possibly located
        """
        self.template_path_list = template_path_list

    def locate_template(self,template_type):
        """Returns the path of a template.

        Given a template type the function will attempt to retrieve its full path. If instead of a template type, a
        full path is given, the function will validate the full path, If the full path cannot be determined, the
        function returns None.

        :param template_type: the type of the template or its full path
        :return: the path of the template or None if it does not exist
        """
        # Ensure we have a template type.
        if not template_type:
            return None

        # Ensure we have a list of paths.
        if not self.template_path_list:
            return None

        # Go through the list of valid paths.
        for path in self.template_path_list:
            base_path = os.path.abspath(path)
            template_path = os.path.join(base_path, template_type)
            is_valid = os.path.exists(template_path)
            if is_valid:
                break

        # Return the full path of the given template or None if it cannot be found.
        return os.path.abspath(template_path) if is_valid else None


    def list_templates(self):
        """Returns a list of available templates ordered alphabetically.

        :return: a list of available templates ordered alphabetically
        """
        # Ensure we have a list of paths.
        if not self.template_path_list:
            return None

        # Initialize an empty set of available templates.
        available_templates = set()

        # Go through the list of valid paths.
        for path in self.template_path_list:
            base_path = os.path.abspath(path)
            try:
                subdirs = os.listdir(base_path)
                available_templates.update(subdirs)
            except FileNotFoundError:
                pass

        # Return a list of available templates ordered alphabetically
        return sorted(available_templates)


def main():
    # Create the parser.
    parser = argparse.ArgumentParser(description="Create a skeleton for your formula.")

    # Create the options.
    parser.add_argument(
        "-n",
        "--name",
        help="the name of your project",
        type=str)
    parser.add_argument(
        "-t",
        "--type",
        help="the type of your template or the path of a jinja template",
        type=str)
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help="output directory (default is the current directory)",
        type=str)
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="list the available templates")

    # Parse the arguments.
    args = parser.parse_args()

    # Create the templetizer object.
    templatizer = Templatizer(template_path_list)

    # List the templates if asked to.
    if args.list:
        print("Available templates: \n\t" + "\n\t".join(templatizer.list_templates()))
        exit(0)

    # Ensure the project name and project type are specified.
    if not args.name or not args.type:
        print("The template type and project name are required: -t type -n name.")
        exit(1)

    # Retrieve the template type.
    template_path = templatizer.locate_template(args.type)
    if not template_path:
        print("The template name you specified does not exist.")
        exit(1)

    # Call the process function
    process(template_path, args.name, args.output)

if __name__ == '__main__':
    main()