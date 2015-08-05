Vagrant-Ansible
===============

To create a skeleton for an ansible provisioned vagrant project::

    saliere vagrant-ansible jenkins -c ~/jenkins-template.yml -o ~/vagrant

Template variables
------------------

This template has 2 sections: one describing the ansible parameters, one describing the VMs parameters.

The ansible section
^^^^^^^^^^^^^^^^^^^

* ``custom_library_paths``: path(s) to your ansibles custom libraries. Separate the paths with colons (':').
* ``custom_role_paths``: path(s) to your ansibles roles. Separate the paths with colons (':').
* ``groups_common``: subsection containing variables and roles to apply to all your groups.

    * ``vars``: dictionary of variables that are common to all your groups.
    * ``provisioning_roles``: list of roles that are common to all your groups.

* ``groups``: subsection caontaining the variables and the roles to apply to specific groups.

    * ``vm_name``: this key is the name of the group to configure.
    * ``provisioning_roles``: list of roles that are common to apply to this groups.

The VM section
^^^^^^^^^^^^^^

* ``memory_size``: the memory size in Megabytes.
* ``vm_synced_folders``: a dictionary of directory to sync. The key is the directory on the guest, the value is directory on the host.
* ``guests``: a list of dictionary describing the guest vms.

    * ``name``: the VM name.
    * ``forwarded_ports``: a dictionary of ports to forward. The key is the port on the guest, the value is port on the host.

Configuration file
------------------

Here is an example of configuration file for the vagrant-ansible skeleton:

.. code-block:: yaml

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

.. note::

    Note that for the ``forwarded_ports`` and ``synced_folders`` sections, the key is **always** the host, and the value the guest.
