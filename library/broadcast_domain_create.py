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
module: broadcast_domain_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create broadcast domain
description:
  - Ansible module to create broadcast domains on NetApp CDOT arrays via the NetApp python SDK.
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
  bc_domain:
    required: True
    description:
      - "Name of the broadcast domain"
  mtu:
    required: True
    description:
      - "MTU of the broadcast domain"
  ports:
    required: True
    description:
      - "List of ports that will be added to the broadcast domain; Format node_name:port_name"


'''

EXAMPLES = '''
# Create broadcast domain
- name: Broadcast domain nfs
    broadcast_domain_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      bc_domain: "nfs"
      mtu: "1500"
      ports: ["atlcdot-01:e0d", "atlcdot-02:e0d"]

'''

def broadcast_domain_create(module):

    bc_domain = module.params['bc_domain']
    mtu = module.params['mtu']
    ports = module.params['ports']

    results = {}
    results['changed'] = False

    api = NaElement("net-port-broadcast-domain-create")
    api.child_add_string("broadcast-domain", bc_domain)
    api.child_add_string("mtu", mtu)

    xi = NaElement("ports")
    api.child_add(xi)

    for port in ports:
        xi.child_add_string("net-qualified-port-name", port)

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
        bc_domain=dict(required=True),
        mtu=dict(required=True),
        ports=dict(required=True, type='list'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = broadcast_domain_create(module)

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




