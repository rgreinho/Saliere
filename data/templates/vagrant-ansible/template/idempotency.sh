#!/bin/bash

VM={{ vm.name }}
PLAYBOOK=ansible/provision.yml

vagrant destroy -f ${VM}
vagrant up ${VM}
ansible-playbook -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=.vagrant/machines/${VM}/virtualbox/private_key -u vagrant -b ${PLAYBOOK} | grep -q 'changed=0.*failed=0' && (echo 'Idempotence test: pass' && exit 0) || (echo 'Idempotence test: fail' && exit 1)
