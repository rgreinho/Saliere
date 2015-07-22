#!/bin/bash

VM={{ vm_name }}
PLAYBOOK=ansible/provision.yml

echo "----------------------------------"
echo " Creating and provisioning the VM
echo "----------------------------------"
vagrant destroy -f ${VM}
vagrant up ${VM}
echo "------------------------------------------------"
echo " Replaying the playbook to test for idempotency
echo "------------------------------------------------"
ansible-playbook -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=.vagrant/machines/${VM}/virtualbox/private_key -u vagrant -b ${PLAYBOOK} | grep -q 'changed=0.*failed=0' && (echo 'Idempotence test: pass' && exit 0) || (echo 'Idempotence test: fail' && exit 1)
