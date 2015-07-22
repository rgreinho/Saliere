Vagrant-Ansible
===============

To create a skeleton for an ansible provisioned vagrant project::

    saliere vagrant-ansible jenkins -c ~/jenkins-template.yml -o ~/vagrant


Configuration file
------------------

Here is an example of configuration file for the vagrant-ansible skeleton:

.. code-block:: yaml

    vagrant-ansible:
        vm:
            name: my_vm
            memory_size: 2048
            forwarded_ports:
                8000: 8000
                8888: 8888
            synced_folders:
                /opt/devstack: ~/projects/devstack
                /opt/scripts: ~/projects/engineering/scripts
        ansible:
            custom_library_paths: library:~/ansible/library
            custom_role_paths: roles:~/ansible/roles

Note that for the ``forwarded_ports`` and ``synced_folders`` sections, the key is **always** the guest, and the value the host.