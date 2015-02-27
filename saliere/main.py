#!/usr/bin/python3
"""Creates a skeleton for various projects based on Jinja2 templates.

Example:

    $ main.py mysql -t salt-formula
    $ main.py mysql-django -t django
    $ main.py mysql -t salt-formula -o my-formula-directory
    $ main.py mysql -t ~/my/custom/template -o my-template-directory
"""

import argparse
import os

from saliere.config import Config
from saliere.templatizer import Templatizer

# Define a list of valid paths to look for the templates
template_path_list = ['templates', '../templates', '/usr/local/share/saliere/templates']


def main():
    # Create the parser.
    parser = argparse.ArgumentParser(description="Create a skeleton for your formula.")

    # Create the options.
    parser.add_argument("-n", "--name", help="the name of your project", type=str)
    parser.add_argument("-t", "--type", help="the type of your template or the path of a jinja template", type=str)
    parser.add_argument("-o", "--output", default=os.getcwd(),
                        help="output directory (default is the current directory)", type=str)
    parser.add_argument("-l", "--list", action="store_true", help="list the available templates")
    parser.add_argument("-c", "--configfile", default='config.yml',
                        help="file containing the template information (default: config.yml)", type=str)
    parser.add_argument("--var", default=None, help="template values", type=str)

    # Parse the arguments.
    args = parser.parse_args()

    # Create the templatizer object.
    t = Templatizer(template_path_list)

    # List the templates if asked to.
    if args.list:
        print("Available templates: \n\t" + "\n\t".join(t.list_templates()))
        exit(0)

    # Ensure the project name and project type are specified.
    if not args.name or not args.type:
        print("The template type and project name are required: -t type -n name.")
        exit(1)

    # Retrieve the template path.
    template_path = t.locate_template(args.type)
    if not template_path:
        print("The template name you specified does not exist.")
        exit(1)

    # Get the project type
    t.template_type = args.type

    # Load the template variables, if any, from the configuration file.
    config = Config()
    config.load_from_file(args.configfile)
    template_vars = config.get_value(args.type)

    # Load the template variables, if any, from the command line.
    if args.var:
        vars_split = args.var.split('|')
        vars_list = [v.split('=', 1) for v in vars_split if '=' in v]
        cli_template_vars = dict(vars_list)

        # And override the values from the config file with the values from the CLI.
        template_vars.update(cli_template_vars)

    # Call the copy function.
    t.copy(args.name, args.output, template_vars)


if __name__ == '__main__':
    main()
