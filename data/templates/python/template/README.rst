{{ project_name }}
================

{{ one_line_summary }}

Install
-------

Using pip::

    $ pip install {{ project_name }}

Read the docs
-------------

The latest documentation is published on Read the Docs: http://{{ project_name }}.readthedocs.org.

Build the docs
--------------

To build the documentation::

    $ pip install sphinx
    $ python setup.py build_sphinx

And then browse to doc/build/html/index.html

Contribute
----------

The repository is located on Github: {{ repository }}.

Formatting
^^^^^^^^^^

For formating the files properly, please use YAPF (https://github.com/google/yapf).

In the root directory of the project, run the following command:

.. code-block:: bash

    yapf -r -i {{ project_name }}/
