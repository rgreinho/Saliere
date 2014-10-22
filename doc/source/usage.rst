Usage
=====

Synopsis
--------

Create a skeleton for your formula.

Usage::

    $ saliere [options] formula

Mandatory positional arguments::

    formula         the name of the formula

Optional arguments::

    -h, --help      show this help message and exit
    -t TEMPLATE, --template TEMPLATE
                    specifies the path of a jinja template
    -o OUTPUT, --output OUTPUT
                    output directory (default is the current directory)

Examples
--------

To simply create a formula in the current directory using the standard template::

$ saliere.py mysql

You can use a specific template with the ``-t`` switch and indicate the path of the template  ::

$ saliere.py mysql -t my-new-amazing-template

You can specify an output directory with the ``-o`` switch followed by the path of the destination::

$ saliere.py mysql -o my-formula_directory

You can also combine them all::

$ saliere.py mysql -t my-new-amazing-template -o my-formula-directory


Template
--------

The default template is based on `the official template from Saltstack <https://github.com/saltstack-formulas/template-formula>`_.

If you want to create the a new template, it is recommended to keep the orginal directory structure, and to only modify the content of the template files and the variables you want to replace.

Links:
------

* **The Salt formula documentation:** http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html
* **The Salt Best Practices:** https://salt.readthedocs.org/en/latest/topics/best_practices.html
