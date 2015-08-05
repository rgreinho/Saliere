#!/usr/bin/python3
"""
Creates a skeleton for your project.

usage:
  saliere [-hlv]
  saliere <type> <name> [-c FILE] [-o DIR] [--var VARS]

arguments:
  type                  the type of your template or the path of a jinja template
  name                  the name of your project

options:
  -c FILE               specify the template configuration file
  -h --help             show this help message and exit
  -l --list             list the available templates
  -o DIR --output=DIR   specify the output directory [default: ./]
  -v --version          show the version information
  --var VARS            define the template variables to use
"""
import os.path

from docopt import docopt
import yaml

from saliere.config import Config
from saliere.templatizer import Templatizer

# Define a list of valid paths to look for the templates
template_path_list = ['data/templates', '../data/templates', '/usr/local/share/saliere/templates']


def load_variables(vars):
    """

    :param vars:
    :returns:
    """
    # Try to load the vars as YAML.
    cli_template_vars = yaml.load(vars)

    # If yaml loads a simple string, we assume we must split it.
    if isinstance(cli_template_vars, str):
        vars_split = cli_template_vars.split('|')
        vars_list = [v.split('=', 1) for v in vars_split if '=' in v]
        return dict(vars_list)
    else:
        return cli_template_vars


def main():
    # Create the parser.
    args = docopt(__doc__, version='Saliere 0.2.0')

    # Create the templatizer object.
    t = Templatizer(template_path_list)

    # List the templates if asked to.
    if args.get('--list'):
        print("Available templates: \n\t" + "\n\t".join(t.list_templates()))
        exit(0)

    # Retrieve the template path.
    template_path = t.locate_template(args.get('<type>'))
    if not template_path:
        print("The template name you specified ('{}') does not exist.".format(args.get('<type>')))
        exit(1)

    # Get the project type.
    t.template_type = args.get('<type>')

    # Load the template variables, if any, from the configuration file.
    config = Config()
    if args.get('-c'):
        config.load_from_file(args.get('-c'))
    template_vars = config.get_value(args.get('<type>'))

    # Load the template variables, if any, from the command line.
    if args.get('--var'):
        # Load the variables and override the values from the config file with the values from the CLI.
        template_vars.update(load_variables(args.get('--var')))

    # Call the copy function.
    t.copy(args.get('<name>'), os.path.expanduser(args.get('--output')), template_vars)


if __name__ == '__main__':
    main()
