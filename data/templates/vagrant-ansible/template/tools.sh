#!/bin/bash

VM={{ vm_name }}
VERBOSITY={{ ansible_verbosity }}
PLAYBOOK=ansible/provision.yml
PLAYBOOK_COMMAND="ansible-playbook -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=.vagrant/machines/${VM}/virtualbox/private_key -u vagrant -b ${PLAYBOOK} ${VERBOSITY}"

if [ $# -lt 1 ]
then
        echo "Usage : $0 (provision | idempotency)"
        exit
fi

case "$1" in
provision)
    echo "---------------------"
    echo " Provisioning the VM "
    echo "---------------------"
    ${PLAYBOOK_COMMAND}
    ;;
idempotency)
    echo "----------------------------------"
    echo " Creating and provisioning the VM"
    echo "----------------------------------"
    vagrant destroy -f ${VM}
    vagrant up ${VM}
    echo "------------------------------------------------"
    echo " Replaying the playbook to test for idempotency"
    echo "------------------------------------------------"
    ${PLAYBOOK_COMMAND} | grep -q 'changed=0.*failed=0' && (echo 'Idempotence test: pass' && exit 0) || (echo 'Idempotence test: fail' && exit 1)
    ;;
*)
    echo "Usage : $0 (provision | idempotency)"
   ;;
esac
