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
VERBOSITY={{ ansible_verbosity }}
{%- endif %}

function usage() {
    echo "Usage : $0 (provision | idempotency) [VM...]"
    exit
}

# Ensure the command was provided.
if [ $# -lt 1 ]; then
    usage
fi

# Check whether we want to run the command against specific VMs only.
if [ ! -z $2 ]; then
    VMS=$2
fi

case "$1" in
provision)
    echo "-------------------------------"
    echo " Provisioning the VM(s) ${VMS} "
    echo "-------------------------------"
    for VM in ${VMS}; do
        ansible-playbook -i ${VAGRANT_INVENTORY} --private-key=.vagrant/machines/${VM}/${VAGRANT_PROVIDER}/private_key -u vagrant -b ${PLAYBOOK} ${VERBOSITY} --limit ${VM}
    done
    ;;
idempotency)
    echo "-------------------------------------------"
    echo " Creating and provisioning the VM(s) ${VMS}"
    echo "-------------------------------------------"
    vagrant destroy -f ${VMS}
    vagrant up ${VMS}
    echo "----------------------------------------------------------"
    echo " Replaying the playbook to test for idempotency for ${VMS}"
    echo "----------------------------------------------------------"
    for VM in ${VMS}; do
        ansible-playbook -i ${VAGRANT_INVENTORY} --private-key=.vagrant/machines/${VM}/${VAGRANT_PROVIDER}/private_key -u vagrant -b ${PLAYBOOK} ${VERBOSITY} --limit ${VM} | grep -q 'changed=0.*failed=0' && (echo "${VM} idempotence test: pass" && exit 0) || (echo "${VM} idempotence test: fail" && exit 1)
    done
    ;;
*)
    usage
   ;;
esac
