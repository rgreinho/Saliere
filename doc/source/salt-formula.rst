Salt-formula
============

To create a skeleton for a Salt formula::

    saliere salt-formula nginx -c ~/salt-formula-template.yml -o ~/salt/formulas

Template variables
------------------

* ``formula_name``: formula name
* ``today``: date of the day

Configuration file
------------------

Here is an example of configuration file for the vagrant-ansible skeleton:

.. code-block:: yaml

    salt-formula:
        formula_name: my-salt-formula
        today: 2015-02-22
