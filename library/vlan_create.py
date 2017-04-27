#!/usr/bin/python

import sys
import json
from  ansible.module_utils import ntap_util

try:
    from NaServer import *
    NASERVER_AVAILABLE = True
except ImportError:
    NASERVER_AVAILABLE = False

if not NASERVER_AVAILABLE:
    module.fail_json(msg="The NetApp Manageability SDK library is not installed")

DOCUMENTATTION = '''
---
module: vlan_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create vlan
description:
  - Ansible module to create vlan interfaces on NetApp CDOT arrays via the NetApp python SDK.
requirements:
  - NetApp Manageability SDK
options:
  cluster:
    required: True
    description:
      - "The ip address or hostname of the cluster"
  user_name:
    required: True
    description:
      - "Administrator user for the cluster/node"
  password:
    required: True
    description:
      - "password for the admin user"
  node:
    required: True
    description:
      - "Name of the ifgrp's node"
  int_name:
    required: True
    description:
      - "Interface that hosts the vlan interface"
  vlanid:
    required: True
    description:
      - "VLAN id"


'''

EXAMPLES = '''
# Create vlan interface e0d-701
- name: Create ifgrp a0a
    ifgrp_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      int_name: "e0d"
      vlanid: "701"

'''

def vlan_create(module):

    node = module.params['node']
    int_name = module.params['int_name']
    vlanid = module.params['vlanid']

    results = {}
    results['changed'] = False

    api = NaElement("net-vlan-create")

    xi = NaElement("vlan-info")
    api.child_add(xi)

    xi.child_add_string('node', node)
    xi.child_add_string('parent-interface', int_name)
    xi.child_add_string('vlanid', vlanid)

    connection = ntap_util.connect_to_api(module)
    xo = connection.invoke_elem(api)

    if(xo.results_errno() != 0):
        r = xo.results_reason()
        module.fail_json(msg=r)
        results['changed'] = False

    else:
        results['changed'] = True

    return results

def main():

    argument_spec = ntap_util.ntap_argument_spec()
    argument_spec.update(dict(
        node=dict(required=True),
        int_name=dict(required=True),
        vlanid=dict(required=True),))

    results = vlan_create(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




