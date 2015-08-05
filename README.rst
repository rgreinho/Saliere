Salière
=======

.. image:: https://requires.io/github/TeamLovely/Saliere/requirements.svg?branch=master
    :target: https://requires.io/github/TeamLovely/Saliere/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://readthedocs.org/projects/saliere/badge/?version=latest
    :target: https://readthedocs.org/projects/saliere/?badge=latest
    :alt: Documentation Status

Salière is a tool giving the ability to easily generate a skeleton for your project.

Install
-------

Using pip::

    $ pip install saliere

Read the docs
-------------

The latest documentation is published on Read the Docs: http://saliere.readthedocs.org.

Build the docs
--------------

To build the documentation::

    $ pip install sphinx
    $ python setup.py build_sphinx

And then browse to doc/build/html/index.html

Contribute
----------

The repository is located on Github: https://github.com/rgreinho/saliere.

Formatting
^^^^^^^^^^

For formating the files properly, please use YAPF (https://github.com/google/yapf).

In the root directory of the project, run the following command:

.. code-block:: bash

    yapf -r -i saliere/
