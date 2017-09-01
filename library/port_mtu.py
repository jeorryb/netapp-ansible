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
module: port_mtu
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Change mtu settings
description:
  - Ansible module to set mtu on NetApp CDOT ports via the NetApp python SDK.
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
      - "Name of node who owns the disks used to create the aggregate"
  port:
    required: True
    description:
      - "Port you are setting flow control settings for"
  mtu:
    required: True
    description:
      - "Desired MTU"


'''

EXAMPLES = '''
# Change MTU
- name: Change mtu for e0d
    port_flow:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      node: "atlcdot-01"
      port: "e0d"
      mtu: "9000"

'''

def port_mtu(module):

    node = module.params['node']
    port = module.params['port']
    mtu = module.params['mtu']

    results = {}
    results['changed'] = False

    api = NaElement("net-port-modify")
    api.child_add_string("mtu", mtu)
    api.child_add_string("node", node)
    api.child_add_string("port", port)

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
        port=dict(required=True),
        mtu=dict(required=True, type='int'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)


    results = port_mtu(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




