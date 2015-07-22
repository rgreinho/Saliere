Vagrant-Ansible
===============

To create a skeleton for an ansible provisioned vagrant project::

    saliere vagrant-ansible jenkins -c ~/jenkins-template.yml -o ~/vagrant

Template variables
------------------

* ``vm_name``: the VM name.
* ``vm_memory_size``: the memory size in Megabytes.
* ``vm_forwarded_ports``: a dictionary of ports to forward. The key is the port on the guest, the value is port on the host.
* ``vm_synced_folders``: a dictionary of directory to sync. The key is the directory on the guest, the value is directory on the host.
* ``ansible_custom_library_paths``: path(s) to your ansibles custom libraries. Separate the paths with colons (':').
* ``ansible_custom_role_paths``: path(s) to your ansibles roles. Separate the paths with colons (':').

Configuration file
------------------

Here is an example of configuration file for the vagrant-ansible skeleton:

.. code-block:: yaml

    vagrant-ansible:
      vm_name: my_vm
      vm_memory_size: 2048
      vm_forwarded_ports:
        8000: 8000
        8888: 8888
      vm_synced_folders:
        /opt/tools: ~/projects/tools
        /opt/scripts: ~/projects/scripts
      ansible_custom_library_paths: library:~/ansible/library
      ansible_custom_role_paths: roles:~/ansible/roles

Note that for the ``forwarded_ports`` and ``synced_folders`` sections, the key is **always** the guest, and the value the host.
