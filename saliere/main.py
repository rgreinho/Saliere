#!/usr/bin/python3
"""
Creates a skeleton for your project.

usage:
  saliere [-hlv]
  saliere <type> <name> [-c FILE] [-o DIR] [--var VARS]

options:
  -c FILE               specify the template configuration file
  -h --help             show this help message and exit
  -l --list             list the available templates
  -n NAME --name=NAME   set the name of your project
  -o DIR --output=DIR   specify the output directory [default: ./]
  -t TYPE --type=TYPE   specify the type of your template or the path of a jinja template
  -v --version          show the version information
  --var VARS            define the template variables to use
"""
import os.path

from docopt import docopt

from saliere.config import Config
from saliere.templatizer import Templatizer

# Define a list of valid paths to look for the templates
template_path_list = ['data/templates', '../data/templates', '/usr/local/share/saliere/templates']


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
        vars_split = args.get('--var').split('|')
        vars_list = [v.split('=', 1) for v in vars_split if '=' in v]
        cli_template_vars = dict(vars_list)

        # And override the values from the config file with the values from the CLI.
        template_vars.update(cli_template_vars)

    # Call the copy function.
    t.copy(args.get('<name>'), os.path.expanduser(args.get('--output')), template_vars)

if __name__ == '__main__':
    main()
