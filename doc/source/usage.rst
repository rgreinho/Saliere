Usage
=====

Synopsis
--------

.. code-block:: bash

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

Usage examples
--------------

Create a Python new vagrant-ansible skeleton::

    saliere vagrant-ansible jenkins -c ~/jenkins-template.yml -o ~/vagrant

Use the default values, but override some of them::

    saliere vagrant-ansible jenkins -c ~/vagrant-ansible-template.yml -o ~/vagrant --var "{ vm: { memory_size: 4096 } }"

The ``--var`` switch supports 2 syntaxes. Either YAML, either pipe separated key=value pairs::

    --var "{ vm_name: enhanced_jenkins, vm_memory_size: 4096 }"
    --var "vm_name=enhanced_jenkins|vm_memory_size:=4096"

Configuration file example
--------------------------

.. code-block:: yaml

    common:
    # Template location. Default values are 'templates', '../templates' and '/usr/local/share/saliere/templates'
    template_path:
    - 'templates'
    - '../templates'
    - 'data/templates'
    - '../data/templates'
    - '/usr/local/share/saliere/templates'
    vagrant-ansible:
        ansible:
            custom_library_paths: library:~/projects/ansible/library
            custom_role_paths: roles:~/projects/ansible/roles
            groups_common:
              vars:
                liquidprompt_apply_all_users: True
              provisioning_roles:
                - sbani.liquidprompt
            groups:
              ci:
                provisioning_roles:
                  - jenkins
                  - jenkins_job_builder
              cibuilder:
                provisioning_roles:
                  - jenkins_bare_slave
                  - jenkins_package_builder
        vm:
            memory_size: 1024
            synced_folders:
              ~/projects/devstack: /opt/devstack
              ~/projects/engineering/scripts: /opt/scripts
            guests:
              - name: cibuilder
              - name: ci
                forwarded_ports:
                  8080: 8080

Templates
---------

Salière is able to generate skeletons for the following project types:

.. toctree::
    :maxdepth: 1

    python
    salt-formula
    vagrant-ansible
