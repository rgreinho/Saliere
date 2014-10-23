#!/usr/bin/python3
"""Create a salt formula skeleton based on Jinja2 templates.

Example:

    $ saliere.py mysql
    $ saliere.py mysql -t my-new-amazing-template
    $ saliere.py mysql -t my-new-amazing-template -o my-formula-directory
"""

import argparse
from datetime import date
import os

import jinja2


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
    """Main function.

    :param template_path: the path of the template to use
    :param formula_name: the name of the formula
    :param output_dir: the path of the output directory
    """
    # Prepare directories
    template_folder_parent = os.path.abspath(os.path.dirname(template_path)) + "/"
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


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Create a skeleton for your formula.")
    parser.add_argument("formula", help="the name of your formula")
    parser.add_argument(
        "-t",
        "--template",
        default="template-formula",
        help="specifies the path of a jinja template",
        type=str)
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help="output directory (default is the current directory)",
        type=str)

    # Parse the arguments
    args = parser.parse_args()

    template_folder = args.template

    # Look for the template in the current directory
    template_exists = os.path.exists(template_folder)

    # Look for the template in /usr/local/share/saliere/templates
    if not template_exists:
        template_folder = os.path.join('/usr/local/share/saliere/templates', args.template)
        template_exists = os.path.exists(template_folder)

    if not template_exists:
        print("The template name you specified does not exist.")
        exit(1)

    # Call the main function
    process(template_folder, args.formula, args.output)

if __name__ == '__main__':
    main()
