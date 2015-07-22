Usage
=====

Synopsis
--------

.. code-block:: bash

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

Templates
---------

Salière is able to generate skeletons for the following project types:

.. toctree::
    :maxdepth: 2

    python
    salt-formula
    vagrant-ansible