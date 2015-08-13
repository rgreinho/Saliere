Python
======

To create a skeleton for an ansible provisioned vagrant project::

    saliere python python_app -c ~/.saliere/python-template.yml -o ~/python
    saliere python python_app  -o ~/python --var "{ project_name: python_app, author: Sam Antha, author_email: sam@antha.com, one_line_summary: The best project ever., license: {type: mit, year: 2015} }"

Template variables
------------------

* ``author``: the name of the author.
* ``author_email``: the email of the author.
* ``license``: a disctionary containing the license details

    * ``type``: the type of license to use: ``mit``, ``apache``, gplv30``
    * ``year``: the license year

* ``one_line_summary``: one line to describe your project.
* ``project_name``: the name of the project.
* ``repository``: the reposiroty of the project.

Configuration file
------------------

Here is an example of configuration file for the python skeleton:

.. code-block:: yaml

    python:
        author: Sam Antha
        author_email: sam@antha.com
        license:
            type: mit
            year: 2015
        one_line_summary: The best project ever!
        project_name: Da best app!
        repository: https://github.com/samantha/dabestapp
