#!/bin/bash

# Define variables.
VMS="
{%- for entry in vm.guests -%}
    {{ entry.name }}{{" "}}
{%- endfor -%}
"
PLAYBOOK=ansible/provision.yml
VAGRANT_INVENTORY=.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory
VAGRANT_PROVIDER=virtualbox
{% if  ansible_verbosity is defined -%}
VERBOSITY=-{{ ansible_verbosity }}
{%- endif %}

# Define functions
play_book(){
    if [ -z $1 ]; then
        echo "Invalid parameter. The name of a VM was expected."
        exit
    fi
    ansible-playbook -i ${VAGRANT_INVENTORY} --private-key=.vagrant/machines/$1/${VAGRANT_PROVIDER}/private_key -u vagrant -b ${PLAYBOOK} ${VERBOSITY} --limit $1
}

usage(){
    echo "Usage : $0 (provision | idempotency) [VM...]"
    exit
}

# Ensure the command was provided.
if [ $# -lt 1 ]; then
    usage
fi

# Check whether we want to run the command against specific VMs only.
if [ ! -z $2 ]; then
    VMS=${@: 2}
fi

case "$1" in
provision)
    for VM in ${VMS}; do
        echo "-------------------------------------------------------------------------------"
        echo " Provisioning ${VM}"
        echo "-------------------------------------------------------------------------------"
        play_book ${VM}
    done
    ;;
idempotency)
    echo "-------------------------------------------------------------------------------"
    echo " (Re)Creating the VM(s): ${VMS}"
    echo "-------------------------------------------------------------------------------"
    vagrant destroy -f ${VMS}
    vagrant up ${VMS}
    for VM in ${VMS}; do
        echo "-------------------------------------------------------------------------------"
        echo " Provisioning ${VM}"
        echo "-------------------------------------------------------------------------------"
        play_book ${VM}
        echo "-------------------------------------------------------------------------------"
        echo " Idempotency test for ${VM}"
        echo "-------------------------------------------------------------------------------"
        play_book ${VM} | grep -q 'changed=0.*failed=0' && (echo "\033[0;32m${VM} idempotence test: pass\033[0m" && exit 0) || (echo "\033[0;31m${VM} idempotence test: fail\033[0m" && exit 1)
    done
    ;;
*)
    usage
   ;;
esac
