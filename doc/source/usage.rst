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

Usage examples
--------------

Create a Python new vagrant-ansible skeleton::

    saliere vagrant-ansible jenkins -c ~/jenkins-template.yml -o ~/vagrant

Use the default values, but override some of them::

    saliere vagrant-ansible jenkins -c ~/vagrant-ansible-template.yml -o ~/vagrant --var "{ vm_name: enhanced_jenkins, vm_memory_size: 4096 }"

The ``--var`` switch supports 2 syntaxes. Either YAML, either pipe separated key=value pairs::

    --var "{ vm_name: enhanced_jenkins, vm_memory_size: 4096 }"
    --var "vm_name=enhanced_jenkins|vm_memory_size:=4096"

Templates
---------

Salière is able to generate skeletons for the following project types:

.. toctree::
    :maxdepth: 1 

    python
    salt-formula
    vagrant-ansible
